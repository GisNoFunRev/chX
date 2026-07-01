"""
Python model 'DiamondDuck_Forecast_v1_Calibrated.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import zidz
from pysd.py_backend.statefuls import Integ, Initial
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2025,
    "final_time": lambda: 2050,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Year",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Historical Urban Land",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_for_lookup": 1},
)
def historical_urban_land():
    return np.interp(
        time_for_lookup(),
        [2000, 2006, 2012, 2018, 2025],
        [154139, 167626, 179759, 181700, 181700],
    )


@component.add(
    name="Urban Land Error Percent",
    units="Percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land_relative_error": 1},
)
def urban_land_error_percent():
    return urban_land_relative_error() * 100


@component.add(
    name="Urban Land Error",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1, "historical_urban_land": 1},
)
def urban_land_error():
    return urban_land() - historical_urban_land()


@component.add(
    name="Urban Land Relative Error",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land_error": 1, "historical_urban_land": 1},
)
def urban_land_relative_error():
    return zidz(urban_land_error(), historical_urban_land())


@component.add(
    name="Urban Land Absolute Error Percent",
    units="Percent",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land_error_percent": 1},
)
def urban_land_absolute_error_percent():
    return float(np.abs(urban_land_error_percent()))


@component.add(
    name="Additional Urban Land Needed for Clearing",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"household_clearing_gap": 1, "land_demand_per_household_q": 1},
)
def additional_urban_land_needed_for_clearing():
    """
    Zusätzliche urbane Fläche, die benötigt würde, um den Household Clearing Gap vollständig zu schliessen.
    """
    return household_clearing_gap() * land_demand_per_household_q()


@component.add(
    name="Mean Annual Housing Cost per Capita",
    units="EUR/Person/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def mean_annual_housing_cost_per_capita():
    """
    Durchschnittliche jährliche Wohnkosten pro Person. Der Monatswert wird auf ein Jahr hochgerechnet.
    """
    return 805 * 12


@component.add(
    name="Aggricultural Land Requirement",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"populational_need_of_kcal_in_km2": 1, "aggricultural_land": 1},
)
def aggricultural_land_requirement():
    """
    Differenz zwischen der benötigten landwirtschaftlichen Fläche für den Kalorienbedarf und der aktuell vorhandenen Aggricultural Land.
    """
    return populational_need_of_kcal_in_km2() - aggricultural_land()


@component.add(
    name="Household Scaling Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_of_households": 1, "reference_initial_number_of_households": 1},
)
def household_scaling_factor():
    """
    Relativer Skalierungsfaktor der Haushaltszahl. Er sorgt dafür, dass die gewünschte urbane Fläche mit der Anzahl Haushalte wächst.
    """
    return number_of_households() / reference_initial_number_of_households()


@component.add(
    name="Current Fringe Rent Gap",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_urban_rent": 1, "agricultural_rent": 1},
)
def current_fringe_rent_gap():
    """
    Current Fringe Rent Gap Positive Differenz zwischen urbaner Miete und landwirtschaftlicher Rente. Wenn Mean Urban Rent höher ist als Agricultural Rent, entsteht ökonomischer Druck zur Umwandlung von landwirtschaftlicher in urbane Fläche. Wenn Agricultural Rent höher ist, wird der Gap auf 0 gesetzt.
    """
    return float(np.maximum(0, mean_urban_rent() - agricultural_rent()))


@component.add(
    name="Current Urban Land per Household",
    units="km2/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1, "number_of_households": 1},
)
def current_urban_land_per_household():
    """
    Current Urban Land per Household Aktuell verfügbare urbane Fläche pro Haushalt. Diese Variable zeigt, wie viel urbane Fläche im Durchschnitt auf einen Haushalt entfällt. Sie ist der zentrale Input für den Land Tightness Index.
    """
    return zidz(urban_land(), number_of_households())


@component.add(
    name="Current Urban Radius",
    units="km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1},
)
def current_urban_radius():
    """
    Aktueller Radius der urbanen Fläche. Die urbane Fläche wird vereinfacht als kreisförmig interpretiert.
    """
    return float(np.sqrt(urban_land() / 3.141))


@component.add(
    name="Urban Fringe Radius",
    units="km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mean_household_income": 1,
        "other_consumption_per_household_z": 1,
        "land_demand_per_household_q": 1,
        "agricultural_rent": 1,
        "transport_cost_per_km_per_household": 1,
    },
)
def urban_fringe_radius():
    """
    Theoretischer AMM-Stadtrand. Der Radius ergibt sich aus der Bedingung, dass die urbane Zahlungsbereitschaft am Rand der landwirtschaftlichen Rente entspricht.
    """
    return float(
        np.maximum(
            0,
            (
                mean_household_income()
                - other_consumption_per_household_z()
                - land_demand_per_household_q() * agricultural_rent()
            )
            / transport_cost_per_km_per_household(),
        )
    )


@component.add(
    name="Share Large City", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def share_large_city():
    """
    Anteil der urbanen Bevölkerung in grossen Städten. Der Wert beschreibt eine vereinfachte Stadtgrössenverteilung und beeinflusst das modellierte Innovationspotenzial.
    """
    return 0.26


@component.add(
    name="AMM Fringe Condition Gap",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_rent_at_fringe": 1, "agricultural_rent": 1},
)
def amm_fringe_condition_gap():
    """
    Differenz zwischen urbaner Rente am AMM-Fringe und Agricultural Rent. Ein Wert nahe null zeigt, dass die Fringe-Bedingung erfüllt ist.
    """
    return urban_rent_at_fringe() - agricultural_rent()


@component.add(
    name="Equivalent Number of Large Cities",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_population_total": 1,
        "representative_large_city_size": 1,
        "share_large_city": 1,
    },
)
def equivalent_number_of_large_cities():
    """
    Modellierte äquivalente Anzahl kleiner Städte. Die urbane Bevölkerung dieser Grössenklasse wird durch eine repräsentative Stadtgrösse geteilt. Es handelt sich nicht um eine echte gezählte Anzahl Städte, sondern um eine vereinfachte Modellgrösse.
    """
    return urban_population_total() * (
        share_large_city() / representative_large_city_size()
    )


@component.add(
    name="Equivalent Number of Medium Cities",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_population_total": 1,
        "representative_medium_city_size": 1,
        "share_medium_city": 1,
    },
)
def equivalent_number_of_medium_cities():
    """
    Modellierte äquivalente Anzahl kleiner Städte. Die urbane Bevölkerung dieser Grössenklasse wird durch eine repräsentative Stadtgrösse geteilt. Es handelt sich nicht um eine echte gezählte Anzahl Städte, sondern um eine vereinfachte Modellgrösse.
    """
    return urban_population_total() * (
        share_medium_city() / representative_medium_city_size()
    )


@component.add(
    name="Equivalent Number of Small Cities",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_population_total": 1,
        "representative_small_city_size": 1,
        "share_small_city": 1,
    },
)
def equivalent_number_of_small_cities():
    """
    Modellierte äquivalente Anzahl kleiner Städte. Die urbane Bevölkerung dieser Grössenklasse wird durch eine repräsentative Stadtgrösse geteilt. Es handelt sich nicht um eine echte gezählte Anzahl Städte, sondern um eine vereinfachte Modellgrösse.
    """
    return urban_population_total() * (
        share_small_city() / representative_small_city_size()
    )


@component.add(
    name="Equivalent Number of Very Large Cities",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "urban_population_total": 1,
        "share_very_large_city": 1,
        "representative_very_large_city_size": 1,
    },
)
def equivalent_number_of_very_large_cities():
    """
    Modellierte äquivalente Anzahl kleiner Städte. Die urbane Bevölkerung dieser Grössenklasse wird durch eine repräsentative Stadtgrösse geteilt. Es handelt sich nicht um eine echte gezählte Anzahl Städte, sondern um eine vereinfachte Modellgrösse.
    """
    return urban_population_total() * (
        share_very_large_city() / representative_very_large_city_size()
    )


@component.add(
    name="Reference Initial Desired Urban Land",
    units="km2",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_initial_desired_urban_land": 1},
    other_deps={
        "_initial_reference_initial_desired_urban_land": {
            "initial": {"desired_urban_land": 1},
            "step": {},
        }
    },
)
def reference_initial_desired_urban_land():
    """
    Initialer Referenzwert der Desired Urban Land. Dieser Wert wird für die Skalierung der synthetischen AMM-Stadt verwendet.
    """
    return _initial_reference_initial_desired_urban_land()


_initial_reference_initial_desired_urban_land = Initial(
    lambda: desired_urban_land(), "_initial_reference_initial_desired_urban_land"
)


@component.add(
    name="Land Conversion Pressure Factors",
    units="km2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"amm_consistent_economic_land_conversion_demand": 1},
)
def land_conversion_pressure_factors():
    """
    Land Conversion Pressure Factors Gesamter modellierter Umwandlungsdruck ohne Soil Protection. Die AMM-basierte Umwandlungsnachfrage wird durch den Rent Gap Pressure Factor verstärkt.
    """
    return amm_consistent_economic_land_conversion_demand()


@component.add(
    name="Spatial Planning",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land_index": 1, "spatial_planing_factor": 1},
)
def spatial_planning():
    """
    Planungsindex aus Urban Land Index und Spacial Planing Factor.
    """
    return urban_land_index() * spatial_planing_factor()


@component.add(
    name="Reference Initial Number of Households",
    units="Household",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_initial_number_of_households": 1},
    other_deps={
        "_initial_reference_initial_number_of_households": {
            "initial": {"number_of_households": 1},
            "step": {},
        }
    },
)
def reference_initial_number_of_households():
    """
    Initialer Referenzwert der Anzahl Haushalte. Er wird verwendet, um die Entwicklung der Haushaltszahl relativ zum Startjahr abzubilden.
    """
    return _initial_reference_initial_number_of_households()


_initial_reference_initial_number_of_households = Initial(
    lambda: number_of_households(), "_initial_reference_initial_number_of_households"
)


@component.add(
    name="Innovation Large",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "equivalent_number_of_large_cities": 1,
        "urban_scaling_exponent_large": 1,
        "representative_large_city_size": 1,
    },
)
def innovation_large():
    """
    Innovationsbeitrag der grossen Stadtklasse. Der Wert folgt der Urban-Scaling-Logik, bei der Innovation überproportional mit der Stadtgrösse skaliert.
    """
    return (
        equivalent_number_of_large_cities()
        * representative_large_city_size() ** urban_scaling_exponent_large()
    )


@component.add(
    name="Innovation Medium",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "equivalent_number_of_medium_cities": 1,
        "representative_medium_city_size": 1,
        "urban_scaling_exponent_medium": 1,
    },
)
def innovation_medium():
    """
    Innovationsbeitrag der mittleren Stadtklasse. Der Wert folgt der Urban-Scaling-Logik, bei der Innovation überproportional mit der Stadtgrösse skaliert.
    """
    return (
        equivalent_number_of_medium_cities()
        * representative_medium_city_size() ** urban_scaling_exponent_medium()
    )


@component.add(
    name="Reference Total Innovation Potential",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_total_innovation_potential": 1},
    other_deps={
        "_initial_reference_total_innovation_potential": {
            "initial": {"total_urban_innovation_potential": 1},
            "step": {},
        }
    },
)
def reference_total_innovation_potential():
    """
    Referenzwert des gesamten Innovationspotenzials zu Beginn der Simulation. Dieser Wert dient zur Normalisierung des späteren Innovationsindex.
    """
    return _initial_reference_total_innovation_potential()


_initial_reference_total_innovation_potential = Initial(
    lambda: total_urban_innovation_potential(),
    "_initial_reference_total_innovation_potential",
)


@component.add(
    name="Innovation very Large",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "equivalent_number_of_very_large_cities": 1,
        "urban_scaling_exponent_very_large": 1,
        "representative_very_large_city_size": 1,
    },
)
def innovation_very_large():
    """
    Innovationsbeitrag der sehr grossen Stadtklasse. Der Wert folgt der Urban-Scaling-Logik, bei der Innovation überproportional mit der Stadtgrösse skaliert.
    """
    return (
        equivalent_number_of_very_large_cities()
        * representative_very_large_city_size() ** urban_scaling_exponent_very_large()
    )


@component.add(
    name="Urban Productivity Effect",
    units="Dmnl/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_productivity_elasticity": 1, "innovation_index": 1},
)
def urban_productivity_effect():
    """
    Urban Productivity Effect Zusätzlicher Produktivitätseffekt auf das Einkommenswachstum. Wenn der Innovation Index über 1 liegt, erhöht sich die Wachstumsrate. Wenn er unter 1 liegt, wird sie reduziert.
    """
    return urban_productivity_elasticity() * (innovation_index() - 1)


@component.add(
    name="Soil Protection Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def soil_protection_factor():
    """
    Soil Protection Factor Stärke der Schutzreaktion auf landwirtschaftliche Knappheit. Je höher dieser Wert ist, desto stärker reduziert steigende landwirtschaftliche Knappheit die spätere Land Conversion Rate.
    """
    return 0.3


@component.add(
    name="Spatial Planing Factor",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def spatial_planing_factor():
    """
    Szenarioparameter für räumliche Planung. Ein Wert von 1 bedeutet eine neutrale Planungsannahme ohne zusätzliche Verstärkung oder Dämpfung.
    """
    return 1.0001


@component.add(
    name="Urban Rent at Current Fringe",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mean_household_income": 1,
        "other_consumption_per_household_z": 1,
        "transport_cost_per_km_per_household": 1,
        "current_urban_radius": 1,
        "land_demand_per_household_q": 1,
    },
)
def urban_rent_at_current_fringe():
    """
    Urbane Rente am aktuellen Stadtrand. Sie ergibt sich aus dem AMM-Budget nach Abzug des sonstigen Konsums und der distanzabhängigen Transportkosten.
    """
    return (
        mean_household_income()
        - other_consumption_per_household_z()
        - transport_cost_per_km_per_household() * current_urban_radius()
    ) / land_demand_per_household_q()


@component.add(
    name="Share Medium City", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def share_medium_city():
    """
    Anteil der urbanen Bevölkerung in mittleren Städten. Der Wert beschreibt eine vereinfachte Stadtgrössenverteilung und beeinflusst das modellierte Innovationspotenzial.
    """
    return 0.2


@component.add(
    name="Share Small City", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def share_small_city():
    """
    Anteil der urbanen Bevölkerung in kleinen Städten. Der Wert beschreibt eine vereinfachte Stadtgrössenverteilung und beeinflusst das modellierte Innovationspotenzial.
    """
    return 0.28


@component.add(
    name="Desired Urban Land",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_fringe_radius": 1},
)
def desired_urban_land():
    """
    Gewünschte urbane Fläche der synthetischen AMM-Stadt. Sie wird aus dem theoretischen Urban Fringe Radius berechnet.
    """
    return 3.141 * urban_fringe_radius() ** 2


@component.add(
    name="Desired Urban Land Total",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_urban_land": 1,
        "urban_aggregate_scale_factor": 1,
        "household_scaling_factor": 1,
    },
)
def desired_urban_land_total():
    """
    Desired Urban Land Total Gesamte gewünschte urbane Fläche. Die Variable ergibt sich aus der gewünschten Landfläche pro Haushalt multipliziert mit der Anzahl Haushalte. Sie ist der zentrale Nachfrageinput für die spätere Urban-Land-Conversion-View.
    """
    return (
        desired_urban_land()
        * urban_aggregate_scale_factor()
        * household_scaling_factor()
    )


@component.add(
    name="Soil Protection Effect",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"max_ceiling_soil_protection": 1, "soil_protection": 1},
)
def soil_protection_effect():
    """
    Begrenzungsfaktor der Boden- und Flächenschutzlogik. Der Effekt reduziert die mögliche Landumwandlung, wird aber durch Max Ceiling Soil Protection begrenzt.
    """
    return float(np.maximum(max_ceiling_soil_protection(), 1 / soil_protection()))


@component.add(
    name="Urban Aggregate Scale Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_initial_urban_land": 1,
        "reference_initial_desired_urban_land": 1,
    },
)
def urban_aggregate_scale_factor():
    """
    Skalierungsfaktor, der die synthetische AMM-Stadt auf die aggregierte urbane Fläche des Gesamtmodells skaliert.
    """
    return reference_initial_urban_land() / reference_initial_desired_urban_land()


@component.add(
    name="Urban Scaling Exponent very Large",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_scaling_exponent_very_large():
    """
    Urban-Scaling-Exponent der sehr grossen Stadtklasse. Werte über 1 bedeuten, dass Innovation überproportional mit der Stadtgrösse steigt.
    """
    return 1.15


@component.add(
    name="Yield",
    units="kcal/km2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"kcal_per_km2_avg_per_t": 1, "innovation_index": 1},
)
def yield_1():
    """
    Yield Landwirtschaftlicher Ertrag pro km2 und Jahr. Da Innovation noch nicht modelliert ist, entspricht Yield vorerst dem Basis-Ertrag "Kcal per km^2 avg per t". Später kann Yield mit dem Innovation Index erweitert werden.
    """
    return kcal_per_km2_avg_per_t() * innovation_index()


@component.add(
    name="Innovation Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "total_urban_innovation_potential": 1,
        "reference_total_innovation_potential": 1,
    },
)
def innovation_index():
    """
    Relativer Innovationsindex. Er vergleicht das aktuelle Total Urban Innovation Potential mit dem initialen Referenzwert.
    """
    return total_urban_innovation_potential() / reference_total_innovation_potential()


@component.add(
    name="Household Capacity of Current Urban Land",
    units="Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1, "land_demand_per_household_q": 1},
)
def household_capacity_of_current_urban_land():
    """
    Anzahl Haushalte, die bei aktueller Urban Land und aktuellem Land Demand per Household theoretisch Platz hätten.
    """
    return urban_land() / land_demand_per_household_q()


@component.add(
    name="Household Clearing Gap",
    units="Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "number_of_households": 1,
        "household_capacity_of_current_urban_land": 1,
    },
)
def household_clearing_gap():
    """
    Positive Differenz zwischen benötigter Haushaltszahl und der Kapazität der aktuellen urbanen Fläche. Negative Werte werden auf null gesetzt.
    """
    return float(
        np.maximum(
            0, number_of_households() - household_capacity_of_current_urban_land()
        )
    )


@component.add(
    name="Innovation Small",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "equivalent_number_of_small_cities": 1,
        "representative_small_city_size": 1,
        "urban_scaling_exponent_small": 1,
    },
)
def innovation_small():
    """
    Innovationsbeitrag der kleinen Stadtklasse. Der Wert folgt der Urban-Scaling-Logik, bei der Innovation überproportional mit der Stadtgrösse skaliert.
    """
    return (
        equivalent_number_of_small_cities()
        * representative_small_city_size() ** urban_scaling_exponent_small()
    )


@component.add(
    name="Urban Population Total",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1, "urban_population_density": 1},
)
def urban_population_total():
    """
    Normalisierte urbane Grössenvariable für den Innovation-Block. Sie wird aus Urban Land und Urban Population Density berechnet.
    """
    return urban_land() / urban_population_density()


@component.add(
    name="Urban Scaling Exponent Medium",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_scaling_exponent_medium():
    """
    Urban-Scaling-Exponent der mittleren Stadtklasse. Werte über 1 bedeuten, dass Innovation überproportional mit der Stadtgrösse steigt.
    """
    return 1.15


@component.add(
    name="Urban Scaling Exponent Small",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_scaling_exponent_small():
    """
    Urban-Scaling-Exponent der kleinen Stadtklasse. Werte über 1 bedeuten, dass Innovation überproportional mit der Stadtgrösse steigt.
    """
    return 1.15


@component.add(
    name="Representative Small City Size",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def representative_small_city_size():
    """
    Repräsentative Stadtgrösse der kleinen Stadtklasse. Der Wert wird zur Approximation der Anzahl kleiner Städte und ihres Innovationsbeitrags verwendet.
    """
    return 100000


@component.add(
    name="Representative Very Large City Size",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def representative_very_large_city_size():
    """
    Repräsentative Stadtgrösse der sehr grossen Stadtklasse. Der Wert wird zur Approximation der Anzahl sehr grosser Städte und ihres Innovationsbeitrags verwendet.
    """
    return 2500000.0


@component.add(
    name="Representative Large City Size",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def representative_large_city_size():
    """
    Repräsentative Stadtgrösse der grossen Stadtklasse. Der Wert wird zur Approximation der Anzahl grosser Städte und ihres Innovationsbeitrags verwendet.
    """
    return 866000


@component.add(
    name="Representative Medium City Size",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def representative_medium_city_size():
    """
    Repräsentative Stadtgrösse der mittleren Stadtklasse. Der Wert wird zur Approximation der Anzahl mittlerer Städte und ihres Innovationsbeitrags verwendet.
    """
    return 316000


@component.add(
    name="Urban Land Required for Households",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_demand_per_household_q": 1, "number_of_households": 1},
)
def urban_land_required_for_households():
    """
    Direkter urbaner Flächenbedarf der Haushalte ohne AMM-Fringe-Skalierung.
    """
    return land_demand_per_household_q() * number_of_households()


@component.add(
    name="Urban Population Density",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_population_density():
    """
    Angenommene urbane Bevölkerungsdichte. Der Wert kann an der EU-OECD-Definition eines Urban Centre mit 1'500 Personen pro km2 orientiert werden.
    """
    return 1500


@component.add(
    name="Share very Large City",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def share_very_large_city():
    """
    Anteil der urbanen Bevölkerung in sehr grossen Städten. Der Wert beschreibt eine vereinfachte Stadtgrössenverteilung und beeinflusst das modellierte Innovationspotenzial.
    """
    return 0.26


@component.add(
    name="Soil Protection",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"spatial_planning": 1, "soil_protection_factor": 1},
)
def soil_protection():
    """
    Dimensionsloser Boden- beziehungsweise Flächenschutzindex aus Spatial Planning und Soil Protection Factor.
    """
    return spatial_planning() * soil_protection_factor()


@component.add(
    name="Land per Capita",
    units="km2/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_per_capita():
    """
    Angenommener urbaner Flächenbedarf pro Person. Der Wert sollte konsistent mit der angenommenen Urban Population Density gewählt werden.
    """
    return 0.0003


@component.add(
    name="Land per Household",
    units="km2/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_per_capita": 1, "mean_household_size": 1},
)
def land_per_household():
    """
    Referenzwert für Landbedarf pro Haushalt. Er ergibt sich aus Land per Capita multipliziert mit Mean Household Size.
    """
    return land_per_capita() * mean_household_size()


@component.add(
    name="Total Urban Innovation Potential",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "innovation_large": 1,
        "innovation_medium": 1,
        "innovation_small": 1,
        "innovation_very_large": 1,
    },
)
def total_urban_innovation_potential():
    """
    Aggregiertes Innovationspotenzial aller Stadtgrössenklassen. Der Wert ergibt sich aus der Summe der klassenspezifischen Innovationsbeiträge.
    """
    return (
        innovation_large()
        + innovation_medium()
        + innovation_small()
        + innovation_very_large()
    )


@component.add(
    name="Urban Rent at Fringe",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "mean_household_income": 1,
        "other_consumption_per_household_z": 1,
        "transport_cost_per_km_per_household": 1,
        "urban_fringe_radius": 1,
        "land_demand_per_household_q": 1,
    },
)
def urban_rent_at_fringe():
    """
    Urbane Rente am theoretischen AMM-Fringe. Diese Variable dient zur Prüfung, ob der berechnete Fringe konsistent mit der Agricultural Rent ist.
    """
    return (
        mean_household_income()
        - other_consumption_per_household_z()
        - transport_cost_per_km_per_household() * urban_fringe_radius()
    ) / land_demand_per_household_q()


@component.add(
    name="Mean Annual Housing Cost per Household",
    units="EUR/Household/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_annual_housing_cost_per_capita": 1, "mean_household_size": 1},
)
def mean_annual_housing_cost_per_household():
    """
    Durchschnittliche jährliche Wohnkosten pro Haushalt. Sie ergeben sich aus den jährlichen Wohnkosten pro Person multipliziert mit der Haushaltsgrösse.
    """
    return mean_annual_housing_cost_per_capita() * mean_household_size()


@component.add(
    name="Urban Scaling Exponent Large",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_scaling_exponent_large():
    """
    Urban-Scaling-Exponent der grossen Stadtklasse. Werte über 1 bedeuten, dass Innovation überproportional mit der Stadtgrösse steigt.
    """
    return 1.15


@component.add(
    name="Number of Households",
    units="Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_population": 1, "mean_household_size": 1},
)
def number_of_households():
    """
    Die Variable verbindet den exogenen Bevölkerungspfad mit der Nachfrage nach Wohnfläche und urbanem Land. Je höher die Bevölkerung oder je kleiner die Haushaltsgrösse, desto mehr Haushalte entstehen.
    """
    return expected_population() / mean_household_size()


@component.add(
    name="Aggricultural Land",
    units="km2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_aggricultural_land": 1},
    other_deps={
        "_integ_aggricultural_land": {
            "initial": {"initial_aggricultural_land": 1},
            "step": {"land_conversion_rate": 1},
        }
    },
)
def aggricultural_land():
    """
    Aggricultural Land Stock für die landwirtschaftliche Fläche. Aggricultural Land sinkt, wenn Fläche in urbane Nutzung umgewandelt wird. Deshalb geht Land Conversion Rate mit negativem Vorzeichen in diesen Stock ein.
    """
    return _integ_aggricultural_land()


_integ_aggricultural_land = Integ(
    lambda: -land_conversion_rate(),
    lambda: initial_aggricultural_land(),
    "_integ_aggricultural_land",
)


@component.add(
    name="Agricultural Rent",
    units="EUR/km2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_agricultural_rent": 1},
    other_deps={
        "_integ_agricultural_rent": {
            "initial": {"initial_agricultural_rent": 1},
            "step": {"agricultural_rent_change": 1},
        }
    },
)
def agricultural_rent():
    """
    Agricultural Rent Stock für die landwirtschaftliche Bodenrente. Die Variable passt sich über Agricultural Rent Change schrittweise an Desired Agricultural Rent an. Agricultural Rent wird später in der AMM- und Urban-Land-Conversion-Logik verwendet.
    """
    return _integ_agricultural_rent()


_integ_agricultural_rent = Integ(
    lambda: agricultural_rent_change(),
    lambda: initial_agricultural_rent(),
    "_integ_agricultural_rent",
)


@component.add(
    name="Agricultural Rent Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agricultural_rent_adjustment_time():
    """
    Agricultural Rent Adjustment Time Anpassungszeit der landwirtschaftlichen Bodenrente. Je höher dieser Wert ist, desto langsamer passt sich Agricultural Rent an Desired Agricultural Rent an.
    """
    return 5


@component.add(
    name="Agricultural Rent Change",
    units="(EUR/km2)/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_agricultural_rent": 1,
        "agricultural_rent": 1,
        "agricultural_rent_adjustment_time": 1,
    },
)
def agricultural_rent_change():
    """
    Agricultural Rent Change Anpassungsrate der landwirtschaftlichen Bodenrente. Sie beschreibt, wie schnell Agricultural Rent auf den gewünschten Rentenwert reagiert.
    """
    return (
        desired_agricultural_rent() - agricultural_rent()
    ) / agricultural_rent_adjustment_time()


@component.add(
    name="Agricultural Rent Sensitivity to Scarcity",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def agricultural_rent_sensitivity_to_scarcity():
    """
    Agricultural Rent Sensitivity to Scarcity Sensitivität der landwirtschaftlichen Bodenrente gegenüber landwirtschaftlicher Knappheit. Ein höherer Wert bedeutet, dass Desired Agricultural Rent stärker auf steigende Relative Agricultural Scarcity reagiert.
    """
    return 1


@component.add(
    name="Agricultural Scarcity Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"populational_need_of_kcal_in_km2": 1, "aggricultural_land": 1},
)
def agricultural_scarcity_index():
    """
    Agricultural Scarcity Index Dimensionsloser Knappheitsindex der landwirtschaftlichen Fläche. Ein Wert von 1 bedeutet, dass die benötigte Fläche ungefähr der verfügbaren Aggricultural Land entspricht. Werte über 1 deuten auf Knappheit hin.
    """
    return zidz(populational_need_of_kcal_in_km2(), aggricultural_land())


@component.add(
    name="AMM Consistent Economic Land Conversion Demand",
    units="km2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land_gap": 1, "urban_expansion_adjustment_time": 1},
)
def amm_consistent_economic_land_conversion_demand():
    """
    AMM Consistent Economic Land Conversion Demand AMM-basierte jährliche Nachfrage nach zusätzlicher urbaner Fläche. Sie ergibt sich aus dem Urban Land Gap geteilt durch die Anpassungszeit der urbanen Expansion.
    """
    return urban_land_gap() / urban_expansion_adjustment_time()


@component.add(
    name="Populational Need of Kcal in Km2",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_kcal_demand": 1, "yield_1": 1},
)
def populational_need_of_kcal_in_km2():
    """
    Target Value: Populational Need of Kcal in Km2 Benötigte landwirtschaftliche Fläche, um den jährlichen Kalorienbedarf der Bevölkerung zu decken. Die Variable ergibt sich aus dem gesamten Kalorienbedarf geteilt durch den Ertrag pro km2.
    """
    return zidz(population_kcal_demand(), yield_1())


@component.add(
    name="Time for Lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "year_unit": 1},
)
def time_for_lookup():
    """
    Time for Lookup Dimensionslose Zeitvariable für Lookup-Funktionen. Da Vensim Lookup-Argumente dimensionslos erwartet, wird Time durch Year Unit geteilt.
    """
    return time() / year_unit()


@component.add(
    name="Initial Aggricultural Land",
    units="km2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_aggricultural_land():
    """
    Initial Aggricultural Land Startwert der landwirtschaftlichen Fläche zu Beginn der Simulation. Dieser Wert initialisiert den Stock Aggricultural Land. Die Fläche sinkt, wenn Land in urbane Nutzung umgewandelt wird.
    """
    return 1600400.0


@component.add(
    name="Caloric Baseline Need pP",
    units="kcal/Person/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def caloric_baseline_need_pp():
    """
    Caloric Baseline Need pP Jährlicher Kalorienbedarf pro Person. Der Wert wird aus einem angenommenen Tagesbedarf von 3400 kcal multipliziert mit 365 Tagen berechnet.
    """
    return 3400 * 365


@component.add(
    name="Cobb Douglas Utility Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "relative_other_consumption_per_household": 1,
        "housing_preference_share_alpha": 2,
        "relative_land_demand_per_household": 1,
    },
)
def cobb_douglas_utility_index():
    """
    Cobb Douglas Utility Index Dimensionsloser Nutzenindex auf Basis einer Cobb-Douglas-Logik. Der Index kombiniert relativen sonstigen Konsum und relative Landnachfrage pro Haushalt. Ein Wert von 1 entspricht dem Nutzen im Startzustand. Werte über 1 zeigen eine Verbesserung gegenüber dem Startzustand, Werte unter 1 eine Verschlechterung.
    """
    return (
        relative_other_consumption_per_household()
        ** (1 - housing_preference_share_alpha())
        * relative_land_demand_per_household() ** housing_preference_share_alpha()
    )


@component.add(
    name="Desired Agricultural Rent",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_agricultural_rent": 1,
        "agricultural_rent_sensitivity_to_scarcity": 1,
        "relative_agricultural_scarcity": 1,
    },
)
def desired_agricultural_rent():
    """
    Desired Agricultural Rent Gewünschte landwirtschaftliche Bodenrente. Sie steigt, wenn Relative Agricultural Scarcity über 1 liegt. Die Sensitivität bestimmt, wie stark die Rente auf Knappheit reagiert.
    """
    return (
        initial_agricultural_rent()
        * relative_agricultural_scarcity()
        ** agricultural_rent_sensitivity_to_scarcity()
    )


@component.add(
    name="Desired Mean Urban Rent",
    units="EUR/km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "initial_mean_urban_rent": 1,
        "urban_rent_sensitivity_to_land_tightness": 1,
        "land_tightness_index": 1,
    },
)
def desired_mean_urban_rent():
    """
    Desired Mean Urban Rent Gewünschte mittlere urbane Miete. Wenn Land Tightness Index über 1 liegt, steigt der gewünschte Mietwert. Wenn der Index unter 1 liegt, sinkt der gewünschte Mietwert. Die Sensitivität bestimmt, wie stark die Miete auf Knappheit reagiert.
    """
    return (
        initial_mean_urban_rent()
        * land_tightness_index() ** urban_rent_sensitivity_to_land_tightness()
    )


@component.add(
    name="Reference Initial Land Demand per Capita",
    units="km2/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def reference_initial_land_demand_per_capita():
    """
    Reference Initial Land Demand per Capita Referenzwert für die urbane Landnachfrage pro Person im Startzustand. 0.000498 km2 entspricht 498 m2 pro Person. Dieser Wert dient zur Kalibrierung der anfänglichen Landnachfrage.
    """
    return 0.000498


@component.add(
    name="Economic Pressure",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"import_dependence": 1},
)
def economic_pressure():
    """
    Economic Pressure Dimensionsloser Druckfaktor aus Import Dependence. Je stärker die Unterdeckung der Nahrungsmittelproduktion ist, desto höher wird dieser Druckfaktor. Er kann später in der Land-Conversion-Logik verwendet werden.
    """
    return 1 + import_dependence() ** 2


@component.add(
    name="Reference Other Consumption Per Household",
    units="EUR/Household",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_other_consumption_per_household": 1},
    other_deps={
        "_initial_reference_other_consumption_per_household": {
            "initial": {"other_consumption_per_household_z": 1},
            "step": {},
        }
    },
)
def reference_other_consumption_per_household():
    """
    Reference Other Consumption Per Household Referenzwert des sonstigen Konsums pro Haushalt zu Beginn der Simulation. Dieser Wert wird verwendet, um den aktuellen Konsum relativ zum Startzustand zu messen.
    """
    return _initial_reference_other_consumption_per_household()


_initial_reference_other_consumption_per_household = Initial(
    lambda: other_consumption_per_household_z(),
    "_initial_reference_other_consumption_per_household",
)


@component.add(
    name="Expected Population",
    units="Person",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time_for_lookup": 1},
)
def expected_population():
    """
    Expected Population Exogener Bevölkerungspfad des Forecast-Modells. Werte 2025-2050 basieren auf Eurostat-Bevölkerungsprojektionen und werden als Baseline-Szenario verwendet.
    """
    return np.interp(
        time_for_lookup(),
        [2025.0, 2030.0, 2035.0, 2040.0, 2045.0, 2050.0],
        [4.518e08, 4.532e08, 4.520e08, 4.500e08, 4.475e08, 4.450e08],
    )


@component.add(
    name="Food Production",
    units="kcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yield_1": 1, "aggricultural_land": 1},
)
def food_production():
    """
    Food Production Jährliche Nahrungsmittelproduktion. Die Variable ergibt sich aus dem landwirtschaftlichen Ertrag pro km2 multipliziert mit der verfügbaren Aggricultural Land.
    """
    return yield_1() * aggricultural_land()


@component.add(
    name="Relative Other Consumption per Household",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "other_consumption_per_household_z": 1,
        "reference_other_consumption_per_household": 1,
    },
)
def relative_other_consumption_per_household():
    """
    Relative Other Consumption per Household Dimensionsloser Index des sonstigen Konsums pro Haushalt. Ein Wert von 1 bedeutet, dass der sonstige Konsum dem Startwert entspricht. Werte über 1 zeigen höheren Konsum, Werte unter 1 tieferen Konsum.
    """
    return zidz(
        other_consumption_per_household_z(), reference_other_consumption_per_household()
    )


@component.add(
    name="Housing Land Expenditure",
    units="EUR/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "housing_preference_share_alpha": 1,
        "disposable_income_after_transport": 1,
    },
)
def housing_land_expenditure():
    """
    Housing Land Expenditure Wohn- bzw. Landbudget eines durchschnittlichen Haushalts. Die Variable ergibt sich aus dem verfügbaren Haushaltseinkommen multipliziert mit dem Housing Preference Share Alpha. Sie bestimmt, wie viel ein Haushalt für urbane Landnutzung ausgeben kann.
    """
    return housing_preference_share_alpha() * disposable_income_after_transport()


@component.add(
    name="Housing Preference Share Alpha",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def housing_preference_share_alpha():
    """
    Housing Preference Share Alpha Anteil des verfügbaren Haushaltseinkommens, der für Wohnen bzw. urbane Landnutzung verwendet wird. Ein Wert von 0.15 bedeutet, dass 15 Prozent des verfügbaren Einkommens für Wohn- und Landkosten eingesetzt werden.
    """
    return 0.15


@component.add(
    name="Import Dependence",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population_kcal_demand": 1, "food_production": 1},
)
def import_dependence():
    """
    Import Dependence Dimensionsloser Indikator für die Abhängigkeit von externer Nahrungsmittelversorgung. Ein Wert von 1 bedeutet, dass die modellierte Food Production den Kalorienbedarf deckt. Werte über 1 zeigen eine Unterdeckung.
    """
    return zidz(population_kcal_demand(), food_production())


@component.add(
    name="Kcal per km2 avg per t",
    units="kcal/km2/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def kcal_per_km2_avg_per_t():
    """
    Kcal per km^2 avg per t Basis-Ertrag landwirtschaftlicher Fläche. Der Wert gibt an, wie viele Kilokalorien pro km2 und Jahr durch landwirtschaftliche Produktion erzeugt werden können. In dieser Modellversion wird dieser Wert vorerst ohne Innovationseffekt verwendet.
    """
    return 1800000000.0


@component.add(
    name="Initial Agricultural Rent",
    units="EUR/km2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_agricultural_rent():
    """
    Initial Agricultural Rent Startwert der landwirtschaftlichen Bodenrente. Dieser Wert initialisiert den Stock Agricultural Rent.
    """
    return 30000


@component.add(
    name="Mean Urban Rent",
    units="EUR/km2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_mean_urban_rent": 1},
    other_deps={
        "_integ_mean_urban_rent": {
            "initial": {"initial_mean_urban_rent": 1},
            "step": {"mean_urban_rent_change": 1},
        }
    },
)
def mean_urban_rent():
    """
    Mean Urban Rent Stock für die mittlere urbane Miete. Die Variable passt sich über Mean Urban Rent Change schrittweise an Desired Mean Urban Rent an. Mean Urban Rent wird später in der AMM-Housing-Demand-View verwendet, um die Landnachfrage pro Haushalt zu berechnen.
    """
    return _integ_mean_urban_rent()


_integ_mean_urban_rent = Integ(
    lambda: mean_urban_rent_change(),
    lambda: initial_mean_urban_rent(),
    "_integ_mean_urban_rent",
)


@component.add(
    name="Mean Urban Rent Change",
    units="(EUR/km2)/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_mean_urban_rent": 1,
        "mean_urban_rent": 1,
        "urban_rent_adjustment_time": 1,
    },
)
def mean_urban_rent_change():
    """
    Mean Urban Rent Change Anpassungsrate der mittleren urbanen Miete. Sie beschreibt, wie schnell Mean Urban Rent auf den gewünschten Mietwert reagiert.
    """
    return (
        desired_mean_urban_rent() - mean_urban_rent()
    ) / urban_rent_adjustment_time()


@component.add(
    name="Land Demand per Household q",
    units="km2/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"housing_land_expenditure": 1, "mean_urban_rent": 1},
)
def land_demand_per_household_q():
    """
    Land Demand per Household q Gewünschte urbane Landfläche pro Haushalt. Die Variable ergibt sich aus dem Wohnbudget pro Haushalt geteilt durch die mittlere urbane Miete pro km2. Je höher das Wohnbudget oder je tiefer die Miete, desto höher ist die Landnachfrage pro Haushalt.
    """
    return zidz(housing_land_expenditure(), mean_urban_rent())


@component.add(
    name="Initial Mean Urban Rent",
    units="EUR/km2",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_initial_mean_urban_rent": 1},
    other_deps={
        "_initial_initial_mean_urban_rent": {
            "initial": {
                "housing_land_expenditure": 1,
                "reference_initial_land_demand_per_household": 1,
            },
            "step": {},
        }
    },
)
def initial_mean_urban_rent():
    """
    Initial Mean Urban Rent Startwert der mittleren urbanen Miete. Der Wert wird aus dem anfänglichen Wohnbudget pro Haushalt und der anfänglichen Referenz-Landnachfrage pro Haushalt berechnet.
    """
    return _initial_initial_mean_urban_rent()


_initial_initial_mean_urban_rent = Initial(
    lambda: housing_land_expenditure() / reference_initial_land_demand_per_household(),
    "_initial_initial_mean_urban_rent",
)


@component.add(
    name="Urban Expansion Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_expansion_adjustment_time():
    """
    Urban Expansion Adjustment Time Anpassungszeit der urbanen Expansion. Je höher dieser Wert ist, desto langsamer wird ein bestehender Urban Land Gap durch neue Landumwandlung geschlossen.
    """
    return 3


@component.add(
    name="Initial Urban Land", units="km2", comp_type="Constant", comp_subtype="Normal"
)
def initial_urban_land():
    """
    Initial Urban Land Startwert der urbanen Fläche zu Beginn der Simulation. Dieser Wert initialisiert den Stock Urban Land.
    """
    return 181700


@component.add(
    name="Reference Agricultural Scarcity Index",
    units="Dmnl",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_agricultural_scarcity_index": 1},
    other_deps={
        "_initial_reference_agricultural_scarcity_index": {
            "initial": {"agricultural_scarcity_index": 1},
            "step": {},
        }
    },
)
def reference_agricultural_scarcity_index():
    """
    Reference Agricultural Scarcity Index Referenzwert des Agricultural Scarcity Index zu Beginn der Simulation. Dieser Wert dient dazu, spätere Knappheit relativ zum Startzustand zu interpretieren.
    """
    return _initial_reference_agricultural_scarcity_index()


_initial_reference_agricultural_scarcity_index = Initial(
    lambda: agricultural_scarcity_index(),
    "_initial_reference_agricultural_scarcity_index",
)


@component.add(
    name="Relative Land Demand per Household",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "land_demand_per_household_q": 1,
        "reference_initial_land_demand_per_household": 1,
    },
)
def relative_land_demand_per_household():
    """
    Relative Land Demand per Household Dimensionsloser Index der Landnachfrage pro Haushalt. Ein Wert von 1 bedeutet, dass die Landnachfrage pro Haushalt dem Startwert entspricht. Werte über 1 zeigen eine höhere, Werte unter 1 eine tiefere Landnachfrage.
    """
    return zidz(
        land_demand_per_household_q(), reference_initial_land_demand_per_household()
    )


@component.add(
    name="Land Conversion Rate",
    units="km2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_conversion_pressure_factors": 1, "max_feasible_conversion": 1},
)
def land_conversion_rate():
    """
    Land Conversion Rate Temporärer Platzhalter für die Landumwandlungsrate. In dieser View wird nur gezeigt, wie die Rate Urban Land erhöht und Aggricultural Land reduziert. Die detaillierte Berechnung von Land Conversion Rate wird später in der Urban-Land-Conversion-View modelliert.
    """
    return float(
        np.minimum(land_conversion_pressure_factors(), max_feasible_conversion())
    )


@component.add(
    name="Land Conversion Time Minimum",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def land_conversion_time_minimum():
    """
    Minimal zulässige Anpassungszeit der Landumwandlung. Der Parameter verhindert unrealistisch schnelle oder numerisch instabile Landkonversion.
    """
    return 1


@component.add(
    name="Land Tightness Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "reference_initial_land_demand_per_household": 1,
        "current_urban_land_per_household": 1,
    },
)
def land_tightness_index():
    """
    Land Tightness Index Dimensionsloser Knappheitsindex für urbane Fläche. Ein Wert von 1 bedeutet, dass die aktuelle urbane Fläche pro Haushalt dem Referenzwert entspricht. Werte über 1 bedeuten höhere Knappheit und erzeugen Druck auf die urbane Miete.
    """
    return zidz(
        reference_initial_land_demand_per_household(),
        current_urban_land_per_household(),
    )


@component.add(
    name="Max Feasible Conversion",
    units="km2/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"aggricultural_land": 1, "land_conversion_time_minimum": 1},
)
def max_feasible_conversion():
    """
    Max Feasible Conversion Maximal mögliche Landumwandlung pro Zeiteinheit. Diese Variable verhindert, dass mehr landwirtschaftliche Fläche umgewandelt wird, als im Modell verfügbar ist.
    """
    return aggricultural_land() / land_conversion_time_minimum()


@component.add(
    name="Reference Initial Land Demand per Household",
    units="km2/Household",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_initial_land_demand_per_household": 1},
    other_deps={
        "_initial_reference_initial_land_demand_per_household": {
            "initial": {
                "initial_mean_household_size": 1,
                "reference_initial_land_demand_per_capita": 1,
            },
            "step": {},
        }
    },
)
def reference_initial_land_demand_per_household():
    """
    Reference Initial Land Demand per Household Referenzwert der urbanen Landnachfrage pro Haushalt zu Beginn der Simulation. Dieser Wert dient als Vergleichswert für die aktuell verfügbare urbane Fläche pro Haushalt.
    """
    return _initial_reference_initial_land_demand_per_household()


_initial_reference_initial_land_demand_per_household = Initial(
    lambda: initial_mean_household_size() * reference_initial_land_demand_per_capita(),
    "_initial_reference_initial_land_demand_per_household",
)


@component.add(
    name="Max Ceiling Soil Protection",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_ceiling_soil_protection():
    """
    Max Ceiling Soil Protection Maximale Reduktion der Landumwandlung durch Soil Protection. Ein Wert von 0.8 bedeutet, dass die Schutzlogik die spätere Land Conversion Rate maximal um 80 Prozent reduzieren kann.
    """
    return 0.8


@component.add(
    name="Reference Initial Urban Land",
    units="km2",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_reference_initial_urban_land": 1},
    other_deps={
        "_initial_reference_initial_urban_land": {
            "initial": {"urban_land": 1},
            "step": {},
        }
    },
)
def reference_initial_urban_land():
    """
    Reference Initial Urban Land Referenzwert der urbanen Fläche zu Beginn der Simulation. Dieser Wert wird verwendet, um relative Veränderungen der urbanen Fläche zu berechnen und spätere Skalierungsfaktoren zu bilden.
    """
    return _initial_reference_initial_urban_land()


_initial_reference_initial_urban_land = Initial(
    lambda: urban_land(), "_initial_reference_initial_urban_land"
)


@component.add(
    name="Urban Land Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urban_land": 1, "reference_initial_urban_land": 1},
)
def urban_land_index():
    """
    Urban Land Index Dimensionsloser Index der urbanen Fläche. Ein Wert von 1 bedeutet, dass Urban Land dem Startwert entspricht. Werte über 1 zeigen eine Zunahme der urbanen Fläche gegenüber dem Startzustand.
    """
    return zidz(urban_land(), reference_initial_urban_land())


@component.add(
    name="Population kcal demand",
    units="kcal/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"caloric_baseline_need_pp": 1, "expected_population": 1},
)
def population_kcal_demand():
    """
    Population kcal demand Gesamter jährlicher Kalorienbedarf der Bevölkerung. Die Variable ergibt sich aus dem jährlichen Kalorienbedarf pro Person multipliziert mit Expected Population.
    """
    return caloric_baseline_need_pp() * expected_population()


@component.add(
    name="Urban Rent Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_rent_adjustment_time():
    """
    Urban Rent Adjustment Time Anpassungszeit der urbanen Miete. Je höher dieser Wert ist, desto langsamer passt sich Mean Urban Rent an Desired Mean Urban Rent an.
    """
    return 2


@component.add(
    name="Urban Rent Sensitivity to Land Tightness",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_rent_sensitivity_to_land_tightness():
    """
    Urban Rent Sensitivity to Land Tightness Sensitivität der urbanen Miete gegenüber Landknappheit. Ein höherer Wert bedeutet, dass Desired Mean Urban Rent stärker auf Änderungen im Land Tightness Index reagiert.
    """
    return 1


@component.add(
    name="Year Unit", units="Year", comp_type="Constant", comp_subtype="Normal"
)
def year_unit():
    """
    Year Unit Technische Hilfsvariable zur Umwandlung von Time in einen dimensionslosen Wert für Lookup-Funktionen.
    """
    return 1


@component.add(
    name="Relative Agricultural Scarcity",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "agricultural_scarcity_index": 1,
        "reference_agricultural_scarcity_index": 1,
    },
)
def relative_agricultural_scarcity():
    """
    Relative Agricultural Scarcity Relative landwirtschaftliche Knappheit gegenüber dem Startzustand. Ein Wert von 1 entspricht der anfänglichen Knappheit. Werte über 1 zeigen zunehmende Knappheit.
    """
    return zidz(agricultural_scarcity_index(), reference_agricultural_scarcity_index())


@component.add(
    name="Other Consumption Per Household z",
    units="EUR/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "housing_preference_share_alpha": 1,
        "disposable_income_after_transport": 1,
    },
)
def other_consumption_per_household_z():
    """
    Other Consumption Per Household z Teil des verfügbaren Haushaltseinkommens, der nicht für Wohnen verwendet wird. Diese Variable repräsentiert den sonstigen Konsum im AMM-Budget und wird später für den Cobb-Douglas Utility Index verwendet.
    """
    return (1 - housing_preference_share_alpha()) * disposable_income_after_transport()


@component.add(
    name="Urban Land Gap",
    units="km2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"desired_urban_land_total": 1, "urban_land": 1},
)
def urban_land_gap():
    """
    Urban Land Gap Differenz zwischen gewünschter und aktuell vorhandener urbaner Fläche. Die MAX-Funktion verhindert negative Werte. Wenn die aktuelle urbane Fläche bereits grösser ist als die gewünschte Fläche, entsteht kein zusätzlicher Umwandlungsdruck.
    """
    return float(np.maximum(0, desired_urban_land_total() - urban_land()))


@component.add(
    name="Rent Gap Pressure Factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"current_fringe_rent_gap": 1, "agricultural_rent": 1},
)
def rent_gap_pressure_factor():
    """
    Rent Gap Pressure Factor Dimensionsloser Druckfaktor aus der Rentendifferenz. Wenn die urbane Miete deutlich über der landwirtschaftlichen Rente liegt, steigt der Druck zur Landumwandlung.
    """
    return 1 + zidz(current_fringe_rent_gap(), agricultural_rent())


@component.add(
    name="Urban Land",
    units="km2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_urban_land": 1},
    other_deps={
        "_integ_urban_land": {
            "initial": {"initial_urban_land": 1},
            "step": {"land_conversion_rate": 1},
        }
    },
)
def urban_land():
    """
    Urban Land Stock für die gesamte urbane Fläche. Urban Land steigt, wenn landwirtschaftliche Fläche in urbane Nutzung umgewandelt wird. Die Veränderung erfolgt über Land Conversion Rate.
    """
    return _integ_urban_land()


_integ_urban_land = Integ(
    lambda: land_conversion_rate(), lambda: initial_urban_land(), "_integ_urban_land"
)


@component.add(
    name="Average Commuting Distance",
    units="km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_commuting_distance():
    """
    Average Commuting Distance Durchschnittliche Pendeldistanz. Diese Distanz wird mit den jährlichen Transportkosten pro Kilometer und Haushalt multipliziert.
    """
    return 14


@component.add(
    name="Average Workdays per Capita",
    units="Dmnl/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_workdays_per_capita():
    """
    Average Workdays per Capita Annualisierungsfaktor für die Transportkosten. Der Wert gibt an, wie viele Arbeitstage bzw. Pendeltage pro Person und Jahr angenommen werden. Der Faktor 2 in der Transportkostenrechnung steht für Hin- und Rückweg.
    """
    return 230


@component.add(
    name="Base Income Growth Rate",
    units="Dmnl/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def base_income_growth_rate():
    """
    Base Income Growth Rate Grundannahme für das jährliche Einkommenswachstum. Dieser Wert gilt unabhängig vom zusätzlichen Produktivitätseffekt.
    """
    return 0.01


@component.add(
    name="Commuters per Household",
    units="Person/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "commuting_share_of_employed_persons": 1,
        "employment_share_of_total_population": 1,
        "mean_household_size": 1,
    },
)
def commuters_per_household():
    """
    Commuters per Household Berechnete Anzahl pendelnder Personen pro Haushalt. Die Variable kombiniert Haushaltsgrösse, Erwerbsquote und Pendleranteil. Sie bestimmt, wie stark Transportkosten auf einen durchschnittlichen Haushalt wirken.Commuters per Household Berechnete Anzahl pendelnder Personen pro Haushalt. Die Variable kombiniert Haushaltsgrösse, Erwerbsquote und Pendleranteil. Sie bestimmt, wie stark Transportkosten auf einen durchschnittlichen Haushalt wirken.
    """
    return (
        commuting_share_of_employed_persons()
        * employment_share_of_total_population()
        * mean_household_size()
    )


@component.add(
    name="Commuting Share of Employed Persons",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def commuting_share_of_employed_persons():
    """
    Commuting Share of Employed Persons Anteil der erwerbstätigen Personen, die regelmässig pendeln. Dieser Wert reduziert die erwerbstätigen Personen auf die tatsächlichen Pendler pro Haushalt.
    """
    return 0.957


@component.add(
    name="Desired Mean Household Size",
    units="Person/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"long_run_mean_household_size": 1},
)
def desired_mean_household_size():
    """
    Desired Mean Household Size Gewünschte bzw. angestrebte Haushaltsgrösse. In dieser Modellversion entspricht sie direkt dem langfristigen Zielwert Long Run Mean Household Size.
    """
    return long_run_mean_household_size()


@component.add(
    name="Desired Transport Cost per km",
    units="EUR/km",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"long_run_transport_cost_per_km": 1},
)
def desired_transport_cost_per_km():
    """
    Desired Transport Cost per km Gewünschter Zielwert der Transportkosten pro Kilometer. In dieser Modellversion entspricht er direkt dem langfristigen Transportkostenwert.
    """
    return long_run_transport_cost_per_km()


@component.add(
    name="Disposable Income after Transport",
    units="EUR/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"mean_household_income": 1, "transport_cost_per_household": 1},
)
def disposable_income_after_transport():
    """
    Disposable Income after Transport Verfügbares Haushaltseinkommen nach Abzug der Transportkosten. Die MAX-Funktion verhindert negative Werte. Diese Variable wird später in der AMM-Budgetlogik auf Wohnen und sonstigen Konsum aufgeteilt.
    """
    return float(
        np.maximum(0, mean_household_income() - transport_cost_per_household())
    )


@component.add(
    name="Employment Share of Total Population",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def employment_share_of_total_population():
    """
    Employment Share of Total Population Anteil der Gesamtbevölkerung, der erwerbstätig ist. Dieser Anteil wird verwendet, um aus der Haushaltsgrösse die potenzielle Anzahl erwerbstätiger Personen pro Haushalt abzuleiten.
    """
    return 0.439


@component.add(
    name="Household Size Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def household_size_adjustment_time():
    """
    Household Size Adjustment Time Anpassungszeit der mittleren Haushaltsgrösse. Je höher dieser Wert ist, desto langsamer bewegt sich Mean Household Size in Richtung des langfristigen Zielwertes.
    """
    return 8


@component.add(
    name="Income per Capita",
    units="EUR/Person",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_income_per_capita": 1},
    other_deps={
        "_integ_income_per_capita": {
            "initial": {"initial_income_per_capita": 1},
            "step": {"income_per_capita_growth": 1},
        }
    },
)
def income_per_capita():
    """
    Income per Capita Stock für das durchschnittliche Einkommen pro Person. Die Variable wächst über Income per Capita Growth und wird durch Initial Income per Capita initialisiert. Sie bildet die Grundlage für das Haushaltseinkommen.
    """
    return _integ_income_per_capita()


_integ_income_per_capita = Integ(
    lambda: income_per_capita_growth(),
    lambda: initial_income_per_capita(),
    "_integ_income_per_capita",
)


@component.add(
    name="Income per Capita Growth",
    units="(EUR/Person)/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"income_per_capita": 1, "net_income_growth_rate": 1},
)
def income_per_capita_growth():
    """
    Income per Capita Growth Wachstumsrate des Einkommens pro Person. Sie ergibt sich aus dem aktuellen Einkommen pro Person multipliziert mit der effektiven jährlichen Einkommenswachstumsrate.
    """
    return income_per_capita() * net_income_growth_rate()


@component.add(
    name="Initial Income per Capita",
    units="EUR/Person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_income_per_capita():
    """
    Initial Income per Capita Startwert des durchschnittlichen Einkommens pro Person. Dieser Wert initialisiert den Stock Income per Capita zu Beginn der Simulation.
    """
    return 41650


@component.add(
    name="Initial Mean Household Size",
    units="Person/Household",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_mean_household_size():
    """
    Initial Mean Household Size Startwert der durchschnittlichen Haushaltsgrösse. Dieser Wert initialisiert den Stock Mean Household Size zu Beginn der Simulation.
    """
    return 2.3


@component.add(
    name="Initial Transport Cost per km",
    units="EUR/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_transport_cost_per_km():
    """
    Initial Transport Cost per km Startwert der Transportkosten pro Kilometer. Dieser Wert initialisiert den Stock Transport Cost per km zu Beginn der Simulation.
    """
    return 0.47


@component.add(
    name="Long Run Mean Household Size",
    units="Person/Household",
    comp_type="Constant",
    comp_subtype="Normal",
)
def long_run_mean_household_size():
    """
    Long Run Mean Household Size Langfristig angenommene durchschnittliche Haushaltsgrösse. Dieser Wert dient als Zielwert, dem sich Mean Household Size über die Zeit annähert.
    """
    return 2.2


@component.add(
    name="Long Run Transport Cost per km",
    units="EUR/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def long_run_transport_cost_per_km():
    """
    Long Run Transport Cost per km Langfristig angenommene Transportkosten pro Kilometer. Dieser Wert dient als Zielwert für Transport Cost per km.
    """
    return 0.47


@component.add(
    name="Maximum Income Growth Rate",
    units="Dmnl/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def maximum_income_growth_rate():
    """
    Maximum Income Growth Rate Obere Grenze für das jährliche Einkommenswachstum. Sie verhindert, dass das Einkommen unrealistisch stark wächst.
    """
    return 0.03


@component.add(
    name="Mean Household Income",
    units="EUR/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"income_per_capita": 1, "mean_household_size": 1},
)
def mean_household_income():
    """
    Mean Household Income Berechnetes durchschnittliches Haushaltseinkommen. Es ergibt sich aus Income per Capita multipliziert mit Mean Household Size. Diese Variable wird später in der AMM-Budgetlogik verwendet.
    """
    return income_per_capita() * mean_household_size()


@component.add(
    name="Mean Household Size",
    units="Person/Household",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_mean_household_size": 1},
    other_deps={
        "_integ_mean_household_size": {
            "initial": {"initial_mean_household_size": 1},
            "step": {"mean_household_size_change": 1},
        }
    },
)
def mean_household_size():
    """
    Mean Household Size Shadow Variable aus View 01. Sie wird hier verwendet, um die Anzahl Pendler pro Haushalt zu berechnen.
    """
    return _integ_mean_household_size()


_integ_mean_household_size = Integ(
    lambda: mean_household_size_change(),
    lambda: initial_mean_household_size(),
    "_integ_mean_household_size",
)


@component.add(
    name="Mean Household Size Change",
    units="Person/Household/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_mean_household_size": 1,
        "mean_household_size": 1,
        "household_size_adjustment_time": 1,
    },
)
def mean_household_size_change():
    """
    Mean Household Size Change Anpassungsrate der mittleren Haushaltsgrösse. Sie beschreibt, wie schnell sich Mean Household Size dem gewünschten langfristigen Wert annähert.
    """
    return (
        desired_mean_household_size() - mean_household_size()
    ) / household_size_adjustment_time()


@component.add(
    name="Minimum Income Growth Rate",
    units="Dmnl/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def minimum_income_growth_rate():
    """
    Minimum Income Growth Rate Untere Grenze für das jährliche Einkommenswachstum. Sie erlaubt negatives Wachstum, begrenzt aber den maximalen Rückgang.
    """
    return -0.02


@component.add(
    name="Net Income Growth Rate",
    units="Dmnl/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "maximum_income_growth_rate": 1,
        "urban_productivity_effect": 1,
        "base_income_growth_rate": 1,
        "minimum_income_growth_rate": 1,
    },
)
def net_income_growth_rate():
    """
    Net Income Growth Rate Effektive jährliche Einkommenswachstumsrate. Die Variable kombiniert die Basiswachstumsrate mit dem Urban Productivity Effect. Durch MIN und MAX wird die Wachstumsrate nach oben und unten begrenzt.
    """
    return float(
        np.minimum(
            maximum_income_growth_rate(),
            float(
                np.maximum(
                    minimum_income_growth_rate(),
                    base_income_growth_rate() + urban_productivity_effect(),
                )
            ),
        )
    )


@component.add(
    name="Transport Cost Adjustment Time",
    units="Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transport_cost_adjustment_time():
    """
    Transport Cost Adjustment Time Anpassungszeit der Transportkosten. Je höher dieser Wert ist, desto langsamer bewegt sich Transport Cost per km in Richtung des langfristigen Zielwertes.
    """
    return 5


@component.add(
    name="Transport Cost per Household",
    units="EUR/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_commuting_distance": 1,
        "transport_cost_per_km_per_household": 1,
    },
)
def transport_cost_per_household():
    """
    Transport Cost per Household Jährliche Transportkosten eines durchschnittlichen Haushalts. Diese Variable wird später in der AMM-Budgetlogik vom Haushaltseinkommen abgezogen und beeinflusst dadurch die verfügbare Wohn- und Konsumnachfrage.
    """
    return average_commuting_distance() * transport_cost_per_km_per_household()


@component.add(
    name="Transport Cost per km",
    units="EUR/km",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_transport_cost_per_km": 1},
    other_deps={
        "_integ_transport_cost_per_km": {
            "initial": {"initial_transport_cost_per_km": 1},
            "step": {"transport_cost_per_km_change": 1},
        }
    },
)
def transport_cost_per_km():
    """
    Transport Cost per km Stock für die durchschnittlichen Transportkosten pro Kilometer. Die Variable verändert sich über die Zeit in Richtung eines langfristigen Zielwertes. Sie bildet die Grundlage für die späteren jährlichen Transportkosten eines Haushalts.
    """
    return _integ_transport_cost_per_km()


_integ_transport_cost_per_km = Integ(
    lambda: transport_cost_per_km_change(),
    lambda: initial_transport_cost_per_km(),
    "_integ_transport_cost_per_km",
)


@component.add(
    name="Transport Cost per km Change",
    units="(EUR/km)/Year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "desired_transport_cost_per_km": 1,
        "transport_cost_per_km": 1,
        "transport_cost_adjustment_time": 1,
    },
)
def transport_cost_per_km_change():
    """
    Transport Cost per km Change Anpassungsrate der Transportkosten pro Kilometer. Sie beschreibt, wie schnell sich Transport Cost per km dem gewünschten langfristigen Wert annähert.
    """
    return (
        desired_transport_cost_per_km() - transport_cost_per_km()
    ) / transport_cost_adjustment_time()


@component.add(
    name="Transport Cost per km per Capita",
    units="EUR/km/Person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_workdays_per_capita": 1, "transport_cost_per_km": 1},
)
def transport_cost_per_km_per_capita():
    """
    Transport Cost per km per Capita Jährliche Transportkosten pro Kilometer und Person. Der Faktor 2 berücksichtigt Hin- und Rückweg. Diese Variable übersetzt die Transportkosten pro Kilometer in eine jährliche Belastung pro pendelnder Person.
    """
    return 2 * average_workdays_per_capita() * transport_cost_per_km()


@component.add(
    name="Transport Cost per km per Household",
    units="EUR/km/Household",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"transport_cost_per_km_per_capita": 1, "commuters_per_household": 1},
)
def transport_cost_per_km_per_household():
    """
    Transport Cost per km per Household Jährliche Transportkosten pro Kilometer und Haushalt. Die Kosten pro Person werden mit der Anzahl Pendler pro Haushalt multipliziert.
    """
    return transport_cost_per_km_per_capita() * commuters_per_household()


@component.add(
    name="Urban Productivity Elasticity",
    units="Dmnl/Year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def urban_productivity_elasticity():
    """
    Urban Productivity Elasticity Sensitivität des Einkommenswachstums gegenüber dem Innovation Index. Je höher dieser Wert ist, desto stärker wirkt sich Innovation auf die Einkommensentwicklung aus.
    """
    return 0.005
