import random


# --------------------------------
# NOMINAL OPERATING POINTS
# --------------------------------

NOMINAL_STATE = {
    "Heart Rate": 82.0,
    "SpO2": 98.0,
    "CO2": 650.0,
    "Root Humidity": 40.0,
    "pH": 6.0,
    "Water Reservoir": 80.0
}


# --------------------------------
# NATURAL VARIATION
# --------------------------------

def apply_nominal_variation(state):

    new_state = state.copy()

    # Strength with which each parameter tends
    # back toward its nominal operating point.
    reversion_strength = 0.15

    # --------------------------------
    # HEART RATE
    # --------------------------------

    new_state["Heart Rate"] += (
        reversion_strength
        * (NOMINAL_STATE["Heart Rate"] - state["Heart Rate"])
        + random.uniform(-2.0, 2.0)
    )

    # --------------------------------
    # SpO2
    # --------------------------------

    new_state["SpO2"] += (
        reversion_strength
        * (NOMINAL_STATE["SpO2"] - state["SpO2"])
        + random.uniform(-0.15, 0.15)
    )

    # --------------------------------
    # CO2
    # --------------------------------

    new_state["CO2"] += (
        reversion_strength
        * (NOMINAL_STATE["CO2"] - state["CO2"])
        + random.uniform(-12.0, 12.0)
    )

    # --------------------------------
    # ROOT HUMIDITY
    # --------------------------------

    new_state["Root Humidity"] += (
        reversion_strength
        * (
            NOMINAL_STATE["Root Humidity"]
            - state["Root Humidity"]
        )
        + random.uniform(-0.7, 0.7)
    )

    # --------------------------------
    # pH
    # --------------------------------

    new_state["pH"] += (
        reversion_strength
        * (NOMINAL_STATE["pH"] - state["pH"])
        + random.uniform(-0.025, 0.025)
    )

    # --------------------------------
    # WATER RESERVOIR
    # --------------------------------

    new_state["Water Reservoir"] += random.uniform(
        -0.25,
        -0.05
    )

    return constrain_state(new_state)

def apply_fault(state, scenario, response_active=False):

    new_state = state.copy()

    # --------------------------------
    # CO2 ACCUMULATION
    # --------------------------------

    if scenario == "CO2":

        new_state["CO2"] += random.uniform(
            70.0,
            100.0
        )


    # --------------------------------
    # LOW CREW OXYGEN
    # --------------------------------

    elif scenario == "LOW_OXYGEN":

        new_state["SpO2"] -= random.uniform(
            0.8,
            1.2
        )


    # --------------------------------
    # HYDROPONIC WATER LOSS
    # --------------------------------

    elif scenario == "WATER_LOSS":

        if not response_active:

            # Major leak before isolation
            new_state["Water Reservoir"] -= random.uniform(
                8.0,
                12.0
            )

        else:

            # Leak successfully isolated.
            # No additional fault-driven water loss.
            pass


    # --------------------------------
    # pH INSTABILITY
    # --------------------------------

    elif scenario == "PH_INSTABILITY":

        new_state["pH"] -= random.uniform(
            0.15,
            0.25
        )


    return constrain_state(new_state)

def apply_response(state, scenario):

    new_state = state.copy()

    # --------------------------------
    # CO2 REMOVAL
    # --------------------------------

    if scenario == "CO2":

        new_state["CO2"] -= random.uniform(
            100.0,
            140.0
        )


    # --------------------------------
    # SUPPLEMENTAL OXYGEN
    # --------------------------------

    elif scenario == "LOW_OXYGEN":

        new_state["SpO2"] += random.uniform(
            1.2,
            1.8
        )


    # --------------------------------
    # pH CORRECTION
    # --------------------------------

    elif scenario == "PH_INSTABILITY":

        new_state["pH"] += random.uniform(
            0.20,
            0.30
        )


    return constrain_state(new_state)

# --------------------------------
# OPERATING LIMITS
# --------------------------------

def constrain_state(state):

    state["Heart Rate"] = max(
        50.0,
        min(160.0, state["Heart Rate"])
    )

    state["SpO2"] = max(
        80.0,
        min(100.0, state["SpO2"])
    )

    state["CO2"] = max(
        300.0,
        min(5000.0, state["CO2"])
    )

    state["Root Humidity"] = max(
        0.0,
        min(100.0, state["Root Humidity"])
    )

    state["pH"] = max(
        0.0,
        min(14.0, state["pH"])
    )

    state["Water Reservoir"] = max(
        0.0,
        min(100.0, state["Water Reservoir"])
    )

    return state