import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

from cultivation import evaluar_cultivo
from life_support import evaluar_soporte_vital

from simulation import (
    NOMINAL_STATE,
    apply_nominal_variation,
    apply_fault,
    apply_response
)

import os

st.write("FINAL APP TEST")
st.write("Running file:", os.path.abspath(__file__))

st.markdown(
    """
    <style>

    /* =========================================================
       MARSGÉNESIS — GLOBAL DESIGN SYSTEM
       6H.3A
       ========================================================= */

    :root {
        --mg-bg: #0E1117;

        --mg-surface: #161B22;
        --mg-surface-secondary: #1C2128;

        --mg-text: #F2F2F2;
        --mg-text-secondary: #D2D5DA;
        --mg-text-muted: #A7ADB7;

        --mg-mars: #B85C38;
        --mg-mars-light: #D9825B;
        --mg-mars-dark: #743A2A;

        --mg-border: #30363D;
    }


    /* =========================================================
       APPLICATION BACKGROUND
       ========================================================= */

    .stApp {
        background-color: var(--mg-bg);
        color: var(--mg-text);
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--mg-bg);
    }

    [data-testid="stMain"] {
        background-color: var(--mg-bg);
    }

    /* STREAMLIT HEADER / TOOLBAR */

    [data-testid="stHeader"] {
        background-color: var(--mg-bg) !important;
    }

    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    [data-testid="stHeader"] * {
        color: var(--mg-text-secondary) !important;
    }


    /* =========================================================
       TYPOGRAPHY
       ========================================================= */

    h1, h2, h3, h4, h5, h6 {
        color: var(--mg-text);
    }

    p {
        color: var(--mg-text-secondary);
    }

    [data-testid="stCaptionContainer"] {
        color: var(--mg-text-muted);
    }

    /* =========================================================
       CONTROL PANEL TYPOGRAPHY
       ========================================================= */

    .st-key-mars_control_panel h2,
    .st-key-mars_control_panel h3 {
        color: var(--mg-text);
        letter-spacing: 0.01em;
    }

    .st-key-mars_control_panel h2 {
        font-size: 1.35rem;
    }

    .st-key-mars_control_panel h3 {
        font-size: 1.15rem;
    }

    /* =========================================================
       CONTROL PANEL — LIVE STATUS
       ========================================================= */

    .mg-control-status {
        width: 100%;
        box-sizing: border-box;
    }


    /* Metadata rows */

    .mg-control-meta-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;

        gap: 0.75rem;
        margin-bottom: 0.45rem;
    }

    .mg-control-meta-label {
        color: var(--mg-text-muted);

        font-size: 0.68rem;
        font-weight: 650;
        letter-spacing: 0.055em;

        text-transform: uppercase;
    }

    .mg-control-meta-value {
        color: var(--mg-text-secondary);

        font-size: 0.80rem;
        font-weight: 500;

        text-align: right;
    }


    /* Phase section */

    .mg-control-phase {
        margin-top: 0.85rem;
        padding-top: 0.75rem;

        border-top: 1px solid var(--mg-border);
    }

    .mg-control-phase-label {
        color: var(--mg-text-muted);

        font-size: 0.68rem;
        font-weight: 650;
        letter-spacing: 0.055em;

        text-transform: uppercase;

        margin-bottom: 0.45rem;
    }


    /* Phase state */

    .mg-control-phase-state {
        display: flex;
        align-items: center;

        gap: 0.55rem;
    }

    .mg-control-phase-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;
        flex-shrink: 0;
    }

    .mg-control-phase-value {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.025em;

        text-transform: uppercase;
    }


    /* NOMINAL */

    .mg-control-nominal .mg-control-phase-dot {
        background-color: #3DDC84;
    }

    .mg-control-nominal .mg-control-phase-value {
        color: #3DDC84;
    }


    /* ACTIVE / PROCESS */

    .mg-control-standby .mg-control-phase-dot {
        background-color: #69A7E8;
    }

    .mg-control-standby .mg-control-phase-value {
        color: #69A7E8;
    }


    /* WARNING / DEGRADED */

    .mg-control-warning .mg-control-phase-dot {
        background-color: #F2B84B;
    }

    .mg-control-warning .mg-control-phase-value {
        color: #F2B84B;
    }


    /* CRITICAL */

    .mg-control-critical .mg-control-phase-dot {
        background-color: #FF5D5D;
    }

    .mg-control-critical .mg-control-phase-value {
        color: #FF5D5D;
    }

    /* =========================================================
       MARSGÉNESIS TITLE
       ========================================================= */

    [data-testid="stMain"] h1 {
        color: var(--mg-text);
        letter-spacing: 0.035em;
        font-weight: 750;
    }

    [data-testid="stMain"] h1::after {
        content: "";
        display: block;

        width: 56px;
        height: 3px;

        margin-top: 0.55rem;

        background-color: var(--mg-mars);
        border-radius: 2px;
    }

    /* =========================================================
       PRIMARY ACTION
       ========================================================= */

    .stButton > button[kind="primary"] {
        background-color: var(--mg-mars);
        border-color: var(--mg-mars);
        color: #F2F2F2;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--mg-mars-light);
        border-color: var(--mg-mars-light);
        color: #F2F2F2;
    }

    .stButton > button[kind="primary"]:focus {
        background-color: var(--mg-mars);
        border-color: var(--mg-mars-light);
        box-shadow: 0 0 0 1px var(--mg-mars-light);
    }

    /* =========================================================
       DIVIDERS
       ========================================================= */

    hr {
        border-color: var(--mg-border);
        opacity: 0.8;
    }


    /* =========================================================
       INPUTS
       ========================================================= */

    /* =========================================================
       SELECTBOX — CLOSED CONTROL
       ========================================================= */

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: var(--mg-surface-secondary) !important;
        background-color: var(--mg-surface-secondary) !important;

        border-color: var(--mg-border) !important;

        color: var(--mg-text) !important;
        -webkit-text-fill-color: var(--mg-text) !important;
    }


    /* Selected value */

    div[data-testid="stSelectbox"]
    div[data-baseweb="select"]
    div[aria-selected="true"] {
        color: var(--mg-text) !important;
        -webkit-text-fill-color: var(--mg-text) !important;
    }


    /* Selectbox text more generally */

    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
        color: var(--mg-text) !important;
        -webkit-text-fill-color: var(--mg-text) !important;
    }


    /* Arrow */

    div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
        fill: var(--mg-text-secondary) !important;
        color: var(--mg-text-secondary) !important;
    }


    /* Focus */

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
        border-color: var(--mg-mars) !important;
        box-shadow: 0 0 0 1px var(--mg-mars-dark) !important;
    }


    /* =========================================================
       SELECTBOX — OPEN DROPDOWN
       ========================================================= */

    div[data-baseweb="popover"] {
        background: var(--mg-surface-secondary) !important;
        background-color: var(--mg-surface-secondary) !important;
    }


    div[data-baseweb="popover"] > div {
        background: var(--mg-surface-secondary) !important;
        background-color: var(--mg-surface-secondary) !important;
    }


    ul[role="listbox"] {
        background: var(--mg-surface-secondary) !important;
        background-color: var(--mg-surface-secondary) !important;
    }


    li[role="option"] {
        background: var(--mg-surface-secondary) !important;
        background-color: var(--mg-surface-secondary) !important;

        color: var(--mg-text-secondary) !important;
        -webkit-text-fill-color: var(--mg-text-secondary) !important;
    }


    /* Text nested inside options */

    li[role="option"] * {
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
    }


    /* Hovered option */

    li[role="option"]:hover {
        background: var(--mg-mars-dark) !important;
        background-color: var(--mg-mars-dark) !important;

        color: var(--mg-text) !important;
        -webkit-text-fill-color: var(--mg-text) !important;
    }


    /* Currently selected option */

    li[role="option"][aria-selected="true"] {
        background: var(--mg-surface) !important;
        background-color: var(--mg-surface) !important;

        color: var(--mg-text) !important;
        -webkit-text-fill-color: var(--mg-text) !important;
    }


    /* =========================================================
       BUTTONS
       ========================================================= */

    .stButton > button {
        background-color: var(--mg-surface-secondary);
        color: var(--mg-text);
        border: 1px solid var(--mg-border);
        border-radius: 6px;

        font-weight: 600;

        transition:
            background-color 0.15s ease,
            border-color 0.15s ease,
            color 0.15s ease;
    }

    .stButton > button:hover {
        background-color: var(--mg-mars-dark);
        border-color: var(--mg-mars);
        color: var(--mg-text);
    }

    .stButton > button:focus {
        border-color: var(--mg-mars-light);
        box-shadow: 0 0 0 1px var(--mg-mars-light);
        color: var(--mg-text);
    }


    /* =========================================================
       EXPANDERS
       ========================================================= */

    [data-testid="stExpander"] {
        background-color: var(--mg-surface);
        border: 1px solid var(--mg-border);
        border-radius: 8px;
    }

    /* =========================================================
       HISTORY EXPANDERS
       6H.4B
       ========================================================= */

    [data-testid="stExpander"] {
        background-color: var(--mg-surface);
        border: 1px solid var(--mg-border);
        border-radius: 8px;
        overflow: hidden;
    }


    /* Expander header */

    [data-testid="stExpander"] summary {
        min-height: 2.65rem;
        padding: 0.15rem 0.75rem;
    }

    [data-testid="stExpander"] summary:hover {
        background-color: var(--mg-surface-secondary);
    }

    [data-testid="stExpander"] summary p {
        color: var(--mg-text-secondary);
        font-size: 0.82rem;
        font-weight: 550;
    }


    /* Arrow */

    [data-testid="stExpander"] summary svg {
        color: var(--mg-text-muted);
        fill: var(--mg-text-muted);
    }


    /* Expanded content */

    [data-testid="stExpanderDetails"] {
        border-top: 1px solid var(--mg-border);
        padding-top: 0.9rem;
    }


    /* =========================================================
    EVENT HISTORY
    ========================================================= */

    .mg-event-history {
        width: 100%;
    }


    /* Individual event */

    .mg-history-event {
        width: 100%;
        box-sizing: border-box;

        padding: 0.8rem 0.9rem;

        border-bottom: 1px solid var(--mg-border);
    }

    .mg-history-event:last-child {
        border-bottom: none;
    }


    /* Top metadata row */

    .mg-history-event-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 1rem;
        margin-bottom: 0.35rem;
    }

    .mg-history-event-title {
        color: var(--mg-text-secondary);

        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.045em;

        text-transform: uppercase;
    }

    .mg-history-event-level {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.045em;

        text-transform: uppercase;
    }


    /* System + time */

    .mg-history-event-meta {
        color: var(--mg-text-muted);

        font-size: 0.72rem;

        margin-bottom: 0.55rem;
    }


    /* Diagnostic message */

    .mg-history-event-message {
        color: var(--mg-text);

        font-size: 0.82rem;
        line-height: 1.4;
    }


    /* Autonomous action */

    .mg-history-event-action {
        margin-top: 0.6rem;
        padding-top: 0.55rem;

        border-top: 1px solid rgba(48, 54, 61, 0.65);
    }

    .mg-history-event-action-label {
        color: var(--mg-text-muted);

        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.055em;

        text-transform: uppercase;

        margin-bottom: 0.18rem;
    }

    .mg-history-event-action-text {
        color: var(--mg-text-secondary);

        font-size: 0.78rem;
        line-height: 1.4;
    }


    /* Semantic event levels */

    .mg-history-warning {
        color: #F2B84B;
    }

    .mg-history-critical {
        color: #FF5D5D;
    }

    .mg-history-action {
        color: #69A7E8;
    }

    .mg-history-success {
        color: #3DDC84;
    }

    .mg-history-nominal {
        color: var(--mg-text-muted);
    }

    /* =========================================================
       FIXED CONTROL PANEL
       ========================================================= */

    .st-key-mars_control_panel {
        position: fixed;
        top: 4.5rem;
        right: max(2rem, calc((100vw - 1120px) / 2));

        width: 245px;
        max-height: calc(100vh - 5.5rem);

        overflow-y: auto;
        z-index: 100;

        background-color: var(--mg-surface);
        border: 1px solid var(--mg-border);
        border-radius: 10px;

        padding: 1rem;
    }


    /* =========================================================
       CONTROL PANEL SCROLLBAR
       ========================================================= */

    .st-key-mars_control_panel::-webkit-scrollbar {
        width: 6px;
    }

    .st-key-mars_control_panel::-webkit-scrollbar-track {
        background: transparent;
    }

    .st-key-mars_control_panel::-webkit-scrollbar-thumb {
        background-color: var(--mg-border);
        border-radius: 10px;
    }

    .st-key-mars_control_panel::-webkit-scrollbar-thumb:hover {
        background-color: var(--mg-text-muted);
    }

    /* =========================================================
       SYSTEM STATUS BANNERS
       ========================================================= */

    .mg-status-banner {
        width: 100%;
        box-sizing: border-box;

        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 1rem;

        background-color: var(--mg-surface);
        border: 1px solid var(--mg-border);
        border-left-width: 4px;

        border-radius: 7px;

        padding: 0.75rem 1rem;
        margin-bottom: 0.65rem;
    }


    /* LEFT SIDE */

    .mg-status-main {
        display: flex;
        align-items: center;

        gap: 0.65rem;
        min-width: 0;
    }


    .mg-status-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;
        flex-shrink: 0;
    }


    .mg-status-label {
        color: var(--mg-text-secondary);

        font-size: 0.78rem;
        font-weight: 650;
        letter-spacing: 0.035em;

        text-transform: uppercase;
    }


    /* RIGHT SIDE */

    .mg-status-value {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.045em;

        text-transform: uppercase;

        white-space: nowrap;
    }


    /* =========================================================
    STATUS SEMANTICS
    ========================================================= */


    /* NOMINAL */

    .mg-banner-nominal {
        border-left-color: #1F6F4A;
    }

    .mg-banner-nominal .mg-status-dot {
        background-color: #3DDC84;
    }

    .mg-banner-nominal .mg-status-value {
        color: #3DDC84;
    }


    /* PROCESS / ACTIVE */

    .mg-banner-standby {
        border-left-color: #275D8C;
    }

    .mg-banner-standby .mg-status-dot {
        background-color: #69A7E8;
    }

    .mg-banner-standby .mg-status-value {
        color: #69A7E8;
    }


    /* WARNING / DEGRADED */

    .mg-banner-warning {
        border-left-color: #8A6418;
    }

    .mg-banner-warning .mg-status-dot {
        background-color: #F2B84B;
    }

    .mg-banner-warning .mg-status-value {
        color: #F2B84B;
    }


    /* CRITICAL */

    .mg-banner-critical {
        border-left-color: #8E2A2D;
    }

    .mg-banner-critical .mg-status-dot {
        background-color: #FF5D5D;
    }

    .mg-banner-critical .mg-status-value {
        color: #FF5D5D;
    }

    /* =========================================================
       TELEMETRY CARDS
       ========================================================= */

    .mg-telemetry-card {
        background-color: var(--mg-surface);
        border: 1px solid var(--mg-border);
        border-radius: 8px;

        width: 96%;
        box-sizing: border-box;

        padding: 0.85rem 1rem;
        min-height: 118px;

        display: flex;
        flex-direction: column;
        justify-content: space-between;

        transition:
            border-color 0.15s ease,
            background-color 0.15s ease;
    }


    /* SYSTEM / SUBSYSTEM LABEL */

    .mg-telemetry-system {
        color: var(--mg-text-muted);

        font-size: 0.70rem;
        font-weight: 650;
        letter-spacing: 0.055em;

        text-transform: uppercase;

        margin-bottom: 0.30rem;
    }


    /* METRIC NAME */

    .mg-telemetry-label {
        color: var(--mg-text-secondary);

        font-size: 0.82rem;
        font-weight: 500;

        line-height: 1.25;
    }


    /* VALUE + STATUS */

    .mg-telemetry-reading {
        display: flex;
        align-items: baseline;
        justify-content: space-between;

        gap: 0.75rem;
        margin-top: 0.75rem;
    }


    /* NUMERIC VALUE */

    .mg-telemetry-value {
        color: var(--mg-text);

        font-size: 1.75rem;
        font-weight: 500;
        line-height: 1;

        letter-spacing: -0.015em;
    }


    /* STATUS INDICATOR */

    .mg-telemetry-dot {
        width: 9px;
        height: 9px;

        border-radius: 50%;
        flex-shrink: 0;
    }


    /* NOMINAL */

    .mg-state-nominal {
        border-color: var(--mg-border);
    }

    .mg-state-nominal .mg-telemetry-dot {
        background-color: #3DDC84;
    }


    /* WARNING */

    .mg-state-warning {
        border-color: #8A6418;
    }

    .mg-state-warning .mg-telemetry-dot {
        background-color: #F2B84B;
    }


    /* CRITICAL */

    .mg-state-critical {
        border-color: #8E2A2D;
    }

    .mg-state-critical .mg-telemetry-dot {
        background-color: #FF5D5D;
    }

    /* =========================================================
       SYSTEM RESPONSE
       ========================================================= */

    .mg-response {
        width: 100%;
        box-sizing: border-box;

        background-color: var(--mg-surface);

        border: 1px solid var(--mg-border);
        border-left-width: 4px;
        border-radius: 8px;

        padding: 0.9rem 1rem;
    }


    /* Header */

    .mg-response-header {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 1rem;

        margin-bottom: 0.7rem;
    }


    .mg-response-system {
        display: flex;
        align-items: center;

        gap: 0.55rem;
    }


    .mg-response-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;
        flex-shrink: 0;
    }


    .mg-response-system-name {
        color: var(--mg-text-secondary);

        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.045em;

        text-transform: uppercase;
    }


    .mg-response-state {
        font-size: 0.70rem;
        font-weight: 700;
        letter-spacing: 0.045em;

        text-transform: uppercase;
    }


    /* Diagnostic message */

    .mg-response-message {
        color: var(--mg-text);

        font-size: 0.86rem;
        font-weight: 500;

        line-height: 1.45;
    }


    /* Autonomous action */

    .mg-response-action {
        margin-top: 0.8rem;
        padding-top: 0.7rem;

        border-top: 1px solid var(--mg-border);
    }


    .mg-response-action-label {
        color: var(--mg-text-muted);

        font-size: 0.66rem;
        font-weight: 700;
        letter-spacing: 0.055em;

        text-transform: uppercase;

        margin-bottom: 0.25rem;
    }


    .mg-response-action-text {
        color: var(--mg-text-secondary);

        font-size: 0.80rem;
        line-height: 1.4;
    }


    /* NOMINAL */

    .mg-response-nominal {
        border-left-color: #1F6F4A;
    }

    .mg-response-nominal .mg-response-dot {
        background-color: #3DDC84;
    }

    .mg-response-nominal .mg-response-state {
        color: #3DDC84;
    }


    /* PROCESS */

    .mg-response-standby {
        border-left-color: #275D8C;
    }

    .mg-response-standby .mg-response-dot {
        background-color: #69A7E8;
    }

    .mg-response-standby .mg-response-state {
        color: #69A7E8;
    }


    /* WARNING */

    .mg-response-warning {
        border-left-color: #8A6418;
    }

    .mg-response-warning .mg-response-dot {
        background-color: #F2B84B;
    }

    .mg-response-warning .mg-response-state {
        color: #F2B84B;
    }


    /* CRITICAL */

    .mg-response-critical {
        border-left-color: #8E2A2D;
    }

    .mg-response-critical .mg-response-dot {
        background-color: #FF5D5D;
    }

    .mg-response-critical .mg-response-state {
        color: #FF5D5D;
    }

    </style>
    """,
    unsafe_allow_html=True
)
 
# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Control del Hábitat MarsGénesis",
    page_icon="🔴",
    layout="wide"
)

# --------------------------------
# SESSION STATE
# --------------------------------

if "response_active" not in st.session_state:
    st.session_state.response_active = False

if "response_system" not in st.session_state:
    st.session_state.response_system = None

if "system_phase" not in st.session_state:
    st.session_state.system_phase = "NOMINAL"

if "simulation_state" not in st.session_state:
    st.session_state.simulation_state = NOMINAL_STATE.copy()

if "scenario" not in st.session_state:
    st.session_state.scenario = "NORMAL"

if "telemetry_history" not in st.session_state:
    st.session_state.telemetry_history = []

if "event_history" not in st.session_state:
    st.session_state.event_history = []

if "current_telemetry" not in st.session_state:
    st.session_state.current_telemetry = None

if "current_events" not in st.session_state:
    st.session_state.current_events = []

if "cycle_number" not in st.session_state:
    st.session_state.cycle_number = 0

if "seismic_phase" not in st.session_state:
    st.session_state.seismic_phase = "INACTIVE"

if "seismic_timer" not in st.session_state:
    st.session_state.seismic_timer = 0

if "response_cycles" not in st.session_state:
    st.session_state.response_cycles = 0

if "previous_event_keys" not in st.session_state:
    st.session_state.previous_event_keys = set()

def log_controller_event(
    event_type,
    level,
    system,
    message,
    action,
    scenario=None
):
    """
    Record a meaningful autonomous-controller event.

    Unlike sensor warnings, controller events represent
    decisions, actions, and state transitions performed
    by the habitat resilience system.
    """

    if scenario is None:
        scenario = st.session_state.scenario

    st.session_state.event_history.append({
        "Time": datetime.now(),
        "Cycle": st.session_state.cycle_number + 1,
        "Scenario": scenario,
        "Event Type": event_type,
        "Level": level,
        "System": system,
        "Message": message,
        "Action": action
    })

def recovery_complete(state, scenario):

    if scenario == "CO2":
        return state["CO2"] <= 750.0

    elif scenario == "LOW_OXYGEN":
        return state["SpO2"] >= 97.0

    elif scenario == "PH_INSTABILITY":
        return 5.7 <= state["pH"] <= 6.3

    return False

def run_monitoring_cycle():

    scenario = st.session_state.scenario
    response_completed_this_cycle = False

    # --------------------------------
    # 1. UPDATE NOMINAL PHYSICAL STATE
    # --------------------------------

    state = apply_nominal_variation(
        st.session_state.simulation_state
    )


    # --------------------------------
    # 2. COUNT ACTIVE RESPONSE CYCLES
    # --------------------------------

    if st.session_state.response_active:
        st.session_state.response_cycles += 1


    # --------------------------------
    # 3. APPLY ACTIVE FAULT
    # --------------------------------

    state = apply_fault(
        state,
        scenario,
        st.session_state.response_active
    )


    # --------------------------------
    # 4. APPLY ACTIVE CORRECTIVE RESPONSE
    # --------------------------------

    if st.session_state.response_active:

        state = apply_response(
            state,
            scenario
        )

        # Water loss is handled by isolation,
        # not by restoring lost water.
        if scenario in [
            "CO2",
            "LOW_OXYGEN",
            "PH_INSTABILITY"
        ]:

            if recovery_complete(
                state,
                scenario
            ):
                st.session_state.response_active = False
                st.session_state.response_system = None
                st.session_state.system_phase = "STABILIZED"

                log_controller_event(
                    event_type="RECOVERY",
                    level="SUCCESS",
                    system="Habitat Controller",
                    message="Affected parameter restored to recovery range.",
                    action=(
                        "Corrective response completed; "
                        "returning habitat to normal monitoring."
                    ),
                    scenario=scenario
                )

                response_completed_this_cycle = True
                st.session_state.scenario = "NORMAL"

            else:
                st.session_state.system_phase = "RECOVERING"


    # --------------------------------
    # 5. WATER-LOSS ISOLATION
    # --------------------------------

    if (
        scenario == "WATER_LOSS"
        and st.session_state.response_active
        and st.session_state.response_cycles >= 1
    ):
        st.session_state.response_active = False
        st.session_state.response_system = None
        st.session_state.system_phase = "STABLE / DEGRADED"

        log_controller_event(
            event_type="ISOLATION",
            level="SUCCESS",
            system="Cultivation",
            message="Suspected hydroponic leak isolated.",
            action=(
                "Fault-driven water loss stopped; "
                "reserve irrigation mode remains active."
            ),
            scenario="WATER_LOSS"
        )

        log_controller_event(
            event_type="RECONFIGURATION",
            level="ACTION",
            system="Cultivation",
            message="Cultivation water system reconfigured.",
            action=(
                "Reserve irrigation mode activated to preserve "
                "remaining water inventory."
            ),
            scenario="WATER_LOSS"
        )

        log_controller_event(
            event_type="STABILIZATION",
            level="SUCCESS",
            system="Habitat Controller",
            message="Water-loss event stabilized.",
            action=(
                "Habitat transitioned to stable degraded operation; "
                "water inventory remains below nominal reserve."
            ),
            scenario="WATER_LOSS"
        )

        response_completed_this_cycle = True
        st.session_state.scenario = "NORMAL"


    # --------------------------------
    # 6. SAVE PHYSICAL STATE
    # --------------------------------

    st.session_state.simulation_state = state


    # --------------------------------
    # 7. READ SENSOR VALUES
    # --------------------------------

    bpm = state["Heart Rate"]
    spo2 = state["SpO2"]
    co2 = state["CO2"]

    humedad = state["Root Humidity"]
    ph = state["pH"]
    tanque = state["Water Reservoir"]


    # --------------------------------
    # 8. HABITAT ENVIRONMENT
    # --------------------------------

    sismo = False

    if scenario == "SEISMIC":

        if st.session_state.seismic_phase == "INACTIVE":
            st.session_state.seismic_phase = "EVENT"
            st.session_state.seismic_timer = 0

        if st.session_state.seismic_phase == "EVENT":
            sismo = True
            st.session_state.seismic_timer += 1


    # --------------------------------
    # 9. SUBSYSTEM EVALUATION
    # --------------------------------

    eventos_cultivo = evaluar_cultivo(
        humedad,
        ph,
        tanque,
        sismo
    )

    eventos_vida = evaluar_soporte_vital(
        bpm,
        spo2,
        co2,
        sismo
    )

    todos_eventos = (
        eventos_vida +
        eventos_cultivo
    )

    # Store the current subsystem events so the interface
    # can display the latest monitoring-cycle results.
    st.session_state.current_events = todos_eventos


    # --------------------------------
    # 10. DETECT WARNINGS
    # --------------------------------

    has_warning = any(
        evento["level"] in ["WARNING", "CRITICAL"]
        for evento in todos_eventos
    )
        # --------------------------------
    # 10A. RECORD NEW DETECTIONS
    # --------------------------------

    current_event_keys = set()

    for evento in todos_eventos:

        if evento["level"] != "NOMINAL":

            event_key = (
                evento["level"],
                evento["system"],
                evento["message"]
            )

            current_event_keys.add(event_key)

            # Record only when this condition was not
            # present during the previous cycle.
            if event_key not in st.session_state.previous_event_keys:

                st.session_state.event_history.append({
                    "Time": datetime.now(),
                    "Cycle": st.session_state.cycle_number + 1,
                    "Scenario": scenario,
                    "Event Type": "DETECTION",
                    "Level": evento["level"],
                    "System": evento["system"],
                    "Message": evento["message"],
                    "Action": evento["action"]
                })

    st.session_state.previous_event_keys = current_event_keys


    # --------------------------------
    # 11. AUTONOMOUS RESPONSE CONTROLLER
    # --------------------------------

    if (
        has_warning
        and scenario in [
            "CO2",
            "LOW_OXYGEN",
            "WATER_LOSS",
            "PH_INSTABILITY"
        ]
        and not st.session_state.response_active
        and not response_completed_this_cycle
    ):

        st.session_state.response_active = True
        st.session_state.response_system = scenario
        st.session_state.response_cycles = 0
        st.session_state.system_phase = "RESPONSE ACTIVE"

        log_controller_event(
            event_type="RESPONSE",
            level="ACTION",
            system="Autonomous Controller",
            message="Anomaly confirmed; autonomous response initiated.",
            action=f"Executing response protocol for {scenario}.",
            scenario=scenario
        )

    elif scenario == "NORMAL":

        st.session_state.response_active = False
        st.session_state.response_system = None

        if state["Water Reservoir"] < 20.0:
            st.session_state.system_phase = "STABLE / DEGRADED"

        elif st.session_state.system_phase == "STABILIZED":
            pass

        else:
            st.session_state.system_phase = "NOMINAL"

    elif (
        not has_warning
        and not st.session_state.response_active
        and st.session_state.system_phase != "STABILIZED"
    ):
        st.session_state.system_phase = "DEGRADING"


    # --------------------------------
    # 12. SEISMIC STATE MACHINE
    # --------------------------------

    if scenario == "SEISMIC":

        if (
            st.session_state.seismic_phase == "EVENT"
            and st.session_state.seismic_timer >= 1
        ):

            log_controller_event(
                event_type="SAFE MODE",
                level="ACTION",
                system="Habitat Controller",
                message="Seismic disturbance confirmed.",
                action=(
                    "Entering protective safe mode; "
                    "critical habitat functions remain under monitoring."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "SAFE_MODE"
            st.session_state.system_phase = "SAFE MODE"

        elif st.session_state.seismic_phase == "SAFE_MODE":

            log_controller_event(
                event_type="PROTECTIVE CONFIGURATION",
                level="ACTION",
                system="Habitat Controller",
                message="Protective safe-mode configuration established.",
                action=(
                    "Maintaining critical life-support monitoring, "
                    "isolating vulnerable fluid systems, and suspending "
                    "nonessential habitat operations."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "ASSESSMENT"
            st.session_state.system_phase = "POST-EVENT ASSESSMENT"

        elif st.session_state.seismic_phase == "ASSESSMENT":

            life_support_available = (
                state["SpO2"] >= 95.0
                and state["CO2"] <= 1000.0
            )

            cultivation_available = (
                state["Root Humidity"] >= 30.0
                and 5.5 <= state["pH"] <= 6.5
            )

            water_available = (
                state["Water Reservoir"] >= 20.0
            )

            # --------------------------------
            # DAMAGED SUBSYSTEM PATHWAY
            # --------------------------------

            if (
                st.session_state.seismic_condition
                == "Cultivation water-loop fault"
            ):

                log_controller_event(
                    event_type="FAULT DETECTION",
                    level="WARNING",
                    system="Cultivation",
                    message=(
                        "Post-seismic assessment detected abnormal "
                        "pressure loss in cultivation water loop."
                    ),
                    action=(
                        "Flagging affected loop for isolation "
                        "and integrity verification."
                    ),
                    scenario="SEISMIC"
                )

                st.session_state.seismic_phase = "FAULT_DETECTED"
                st.session_state.system_phase = "FAULT DETECTED"

            # --------------------------------
            # NO-DAMAGE PATHWAY
            # --------------------------------

            elif (
                life_support_available
                and cultivation_available
                and water_available
            ):

                log_controller_event(
                    event_type="ASSESSMENT",
                    level="SUCCESS",
                    system="Habitat Controller",
                    message="Post-event functional assessment completed.",
                    action=(
                        "Life support, cultivation, and water systems "
                        "remain within operational limits."
                    ),
                    scenario="SEISMIC"
                )

                st.session_state.seismic_phase = "VERIFIED"
                st.session_state.system_phase = "VERIFIED"

        elif st.session_state.seismic_phase == "FAULT_DETECTED":

            log_controller_event(
                event_type="FAULT ISOLATION",
                level="ACTION",
                system="Cultivation",
                message=(
                    "Damaged cultivation water-loop segment identified."
                ),
                action=(
                    "Closing isolation valves around affected segment "
                    "to prevent further fluid loss."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "ISOLATED"
            st.session_state.system_phase = "FAULT ISOLATED"

        elif st.session_state.seismic_phase == "ISOLATED":

            log_controller_event(
                event_type="RECONFIGURATION",
                level="ACTION",
                system="Cultivation",
                message=(
                    "Primary cultivation water-loop segment unavailable."
                ),
                action=(
                    "Opening redundant bypass and rerouting "
                    "cultivation water service around isolated segment."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "RECONFIGURED"
            st.session_state.system_phase = "DEGRADED OPERATION"

        elif st.session_state.seismic_phase == "RECONFIGURED":

            cultivation_service_available = (
                state["Root Humidity"] >= 30.0
                and state["Water Reservoir"] >= 20.0
            )

            if cultivation_service_available:

                log_controller_event(
                    event_type="FUNCTIONAL VERIFICATION",
                    level="SUCCESS",
                    system="Cultivation",
                    message=(
                        "Cultivation water service maintained "
                        "through redundant bypass."
                    ),
                    action=(
                        "Post-reconfiguration telemetry confirms "
                        "continued cultivation water availability."
                    ),
                    scenario="SEISMIC"
                )

                st.session_state.seismic_phase = "BYPASS_VERIFIED"
                st.session_state.system_phase = "REDUNDANCY VERIFIED"

        elif st.session_state.seismic_phase == "BYPASS_VERIFIED":

            log_controller_event(
                event_type="RESILIENCE CONFIRMATION",
                level="SUCCESS",
                system="Habitat Controller",
                message=(
                    "Post-seismic habitat functionality confirmed "
                    "under degraded configuration."
                ),
                action=(
                    "Maintaining cultivation water service through "
                    "redundant bypass; primary loop flagged for maintenance."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "RESILIENT_OPERATION"
            st.session_state.system_phase = "RESILIENT OPERATION"

        elif st.session_state.seismic_phase == "VERIFIED":

            log_controller_event(
                event_type="VERIFICATION",
                level="SUCCESS",
                system="Habitat Controller",
                message="Critical habitat functions verified operational.",
                action=(
                    "Exiting protective configuration and "
                    "resuming nominal autonomous monitoring."
                ),
                scenario="SEISMIC"
            )

            st.session_state.seismic_phase = "INACTIVE"
            st.session_state.seismic_timer = 0
            st.session_state.scenario = "NORMAL"
            st.session_state.system_phase = "STABILIZED"


    # --------------------------------
    # 13. RECORD TELEMETRY
    # --------------------------------

    timestamp = datetime.now()

    telemetry = {
        "Time": timestamp,
        "Heart Rate": bpm,
        "SpO2": spo2,
        "CO2": co2,
        "Root Humidity": humedad,
        "pH": ph,
        "Water Reservoir": tanque,
        "Scenario": scenario
    }

    st.session_state.current_telemetry = telemetry

    st.session_state.telemetry_history.append(
        telemetry
    )


    # --------------------------------
    # 15. ADVANCE SIMULATION
    # --------------------------------

    st.session_state.cycle_number += 1

if st.session_state.current_telemetry is None:
    run_monitoring_cycle()

telemetry = st.session_state.current_telemetry

bpm = telemetry["Heart Rate"]
spo2 = telemetry["SpO2"]
co2 = telemetry["CO2"]
humedad = telemetry["Root Humidity"]
ph = telemetry["pH"]
tanque = telemetry["Water Reservoir"]

todos_eventos = st.session_state.current_events
levels = [
    evento["level"]
    for evento in todos_eventos
]

if "CRITICAL" in levels:
    habitat_status = "CRITICAL"

elif "WARNING" in levels:
    habitat_status = "WARNING"

else:
    habitat_status = "NOMINAL"

# --------------------------------
# DISPLAY / INTERFACE
# --------------------------------

# --------------------------------
# TITLE
# --------------------------------

st.title("HABITAT MARSGÉNESIS")
st.subheader("Demostración de Monitoreo Autónomo y Resiliencia de Sistemas")

# --------------------------------
# DASHBOARD LAYOUT
# --------------------------------

main_col, control_col = st.columns(
    [3, 1],
    gap="large"
)

# --------------------------------
# CONTROL CONSOLE STATUS
# --------------------------------

scenario_display_names = {
    "NORMAL": "Operación Normal",
    "SEISMIC": "Evento Sísmico",
    "CO2": "Acumulación de CO₂",
    "LOW_OXYGEN": "Bajo nivel de oxígeno de la tripulación",
    "WATER_LOSS": "Pérdida de agua hidropónica",
    "PH_INSTABILITY": "Inestabilidad de pH"
}

system_phase_display_names = {
    "NOMINAL": "NOMINAL",
    "DEGRADING": "DEGRADACIÓN",
    "RESPONSE ACTIVE": "RESPUESTA ACTIVA",
    "RECOVERING": "RECUPERACIÓN",
    "STABILIZED": "ESTABILIZADO",
    "STABLE / DEGRADED": "ESTABLE / DEGRADADO",
    "SAFE MODE": "MODO SEGURO",
    "POST-EVENT ASSESSMENT": "EVALUACIÓN POSTEVENTO",
    "FAULT DETECTED": "FALLA DETECTADA",
    "FAULT ISOLATED": "FALLA AISLADA",
    "DEGRADED OPERATION": "OPERACIÓN DEGRADADA",
    "REDUNDANCY VERIFIED": "REDUNDANCIA VERIFICADA",
    "RESILIENT OPERATION": "OPERACIÓN RESILIENTE",
    "VERIFIED": "VERIFICADO"
}

# --------------------------------
# EVENT DISPLAY TRANSLATIONS
# --------------------------------

event_type_display_names = {
    "DETECTION": "DETECCIÓN",
    "RESPONSE": "RESPUESTA",
    "RECOVERY": "RECUPERACIÓN",
    "ISOLATION": "AISLAMIENTO",
    "RECONFIGURATION": "RECONFIGURACIÓN",
    "STABILIZATION": "ESTABILIZACIÓN",
    "SAFE MODE": "MODO SEGURO",
    "PROTECTIVE CONFIGURATION": "CONFIGURACIÓN DE PROTECCIÓN",
    "ASSESSMENT": "EVALUACIÓN",
    "FAULT DETECTION": "DETECCIÓN DE FALLA",
    "FAULT ISOLATION": "AISLAMIENTO DE FALLA",
    "FUNCTIONAL VERIFICATION": "VERIFICACIÓN FUNCIONAL",
    "RESILIENCE CONFIRMATION": "CONFIRMACIÓN DE RESILIENCIA",
    "VERIFICATION": "VERIFICACIÓN"
}

level_display_names = {
    "NOMINAL": "NOMINAL",
    "WARNING": "ADVERTENCIA",
    "CRITICAL": "CRÍTICO",
    "ACTION": "ACCIÓN",
    "SUCCESS": "EXITOSO"
}

system_display_names = {
    "Habitat Controller": "Controlador del Hábitat",
    "Autonomous Controller": "Controlador Autónomo",
    "Cultivation": "Cultivo",
    "Life Support": "Soporte Vital",
    "Atmosphere": "Atmósfera",
    "Crew Health": "Salud de la Tripulación"
}

message_display_names = {
    "Affected parameter restored to recovery range.":
        "Parámetro afectado restaurado al rango de recuperación.",

    "Suspected hydroponic leak isolated.":
        "Fuga hidropónica sospechada aislada.",

    "Cultivation water system reconfigured.":
        "Sistema de agua de cultivo reconfigurado.",

    "Water-loss event stabilized.":
        "Evento de pérdida de agua estabilizado.",

    "Anomaly confirmed; autonomous response initiated.":
        "Anomalía confirmada; respuesta autónoma iniciada.",

    "Seismic disturbance confirmed.":
        "Perturbación sísmica confirmada.",

    "Protective safe-mode configuration established.":
        "Configuración de modo seguro de protección establecida.",

    "Post-seismic assessment detected abnormal pressure loss in cultivation water loop.":
        "La evaluación postsísmica detectó una pérdida anormal de presión en el circuito de agua del sistema de cultivo.",

    "Post-event functional assessment completed.":
        "Evaluación funcional postevento completada.",

    "Damaged cultivation water-loop segment identified.":
        "Segmento dañado del circuito de agua del sistema de cultivo identificado.",

    "Primary cultivation water-loop segment unavailable.":
        "Segmento primario del circuito de agua del sistema de cultivo no disponible.",

    "Cultivation water service maintained through redundant bypass.":
        "Suministro de agua al sistema de cultivo mantenido mediante el bypass redundante.",

    "Post-seismic habitat functionality confirmed under degraded configuration.":
        "Funcionalidad postsísmica del hábitat confirmada bajo configuración degradada.",

    "Critical habitat functions verified operational.":
        "Funciones críticas del hábitat verificadas como operativas.",

    "Seismic event detected.":
        "Evento sísmico detectado.",

    "Seismic vibration detected.":
        "Vibración sísmica detectada.",
}

action_display_names = {
    "Corrective response completed; returning habitat to normal monitoring.":
        "Respuesta correctiva completada; el hábitat regresa al monitoreo normal.",

    "Fault-driven water loss stopped; reserve irrigation mode remains active.":
        "Pérdida de agua causada por la falla detenida; el modo de irrigación de reserva permanece activo.",

    "Reserve irrigation mode activated to preserve remaining water inventory.":
        "Modo de irrigación de reserva activado para preservar el agua restante.",

    "Habitat transitioned to stable degraded operation; water inventory remains below nominal reserve.":
        "El hábitat pasó a operación degradada estable; la reserva de agua permanece por debajo del nivel nominal.",

    "Entering protective safe mode; critical habitat functions remain under monitoring.":
        "Activando modo seguro de protección; las funciones críticas del hábitat permanecen bajo monitoreo.",

    "Maintaining critical life-support monitoring, isolating vulnerable fluid systems, and suspending nonessential habitat operations.":
        "Manteniendo el monitoreo crítico de soporte vital, aislando sistemas de fluidos vulnerables y suspendiendo operaciones no esenciales del hábitat.",

    "Flagging affected loop for isolation and integrity verification.":
        "Marcando el circuito afectado para aislamiento y verificación de integridad.",

    "Life support, cultivation, and water systems remain within operational limits.":
        "Los sistemas de soporte vital, cultivo y agua permanecen dentro de los límites operativos.",

    "Closing isolation valves around affected segment to prevent further fluid loss.":
        "Cerrando válvulas de aislamiento alrededor del segmento afectado para evitar pérdidas adicionales de fluido.",

    "Opening redundant bypass and rerouting cultivation water service around isolated segment.":
        "Abriendo el bypass redundante y redirigiendo el suministro de agua de cultivo alrededor del segmento aislado.",

    "Post-reconfiguration telemetry confirms continued cultivation water availability.":
        "La telemetría posterior a la reconfiguración confirma la disponibilidad continua de agua para cultivo.",

    "Maintaining cultivation water service through redundant bypass; primary loop flagged for maintenance.":
        "Manteniendo el suministro de agua al sistema de cultivo mediante el bypass redundante; circuito primario marcado para mantenimiento.",

    "Exiting protective configuration and resuming nominal autonomous monitoring.":
        "Saliendo de la configuración de protección y reanudando el monitoreo autónomo nominal.",

    "Activating backup ventilation and CO2 removal.":
        "Activando ventilación de respaldo y eliminación de CO₂.",

    "Activating supplemental oxygen at crew workstation.":
        "Activando oxígeno suplementario en la estación de la tripulación.",

    "Isolating suspected leak and activating reserve irrigation mode.":
        "Aislando la fuga sospechada y activando el modo de irrigación de reserva.",

    "Activating chemical dosing system.":
        "Activando el sistema de dosificación química.",

    "Adjusting environmental lighting and activating crew support protocol.":
        "Ajustando la iluminación ambiental y activando el protocolo de apoyo a la tripulación.",

    "Closing solenoid valves and isolating fluids.":
        "Cerrando válvulas solenoides y aislando los circuitos de fluidos.",
}

def translate_display(value, mapping):
    return mapping.get(value, value)


def translate_action(action):
    if action.startswith("Executing response protocol for "):
        scenario_code = (
            action
            .replace("Executing response protocol for ", "")
            .rstrip(".")
        )

        scenario_name = scenario_display_names.get(
            scenario_code,
            scenario_code
        )

        return f"Ejecutando protocolo de respuesta para {scenario_name}."

    return action_display_names.get(action, action)


def translate_display(value, mapping):
    return mapping.get(value, value)


def translate_message(message):

    # Exact controller-generated messages
    if message in message_display_names:
        return message_display_names[message]

    # Dynamic CO₂ warning
    if message.startswith("Elevated CO2 detected:"):
        value = message.replace(
            "Elevated CO2 detected:", ""
        ).strip()

        return f"CO₂ elevado detectado: {value}"

    # Dynamic SpO₂ warning
    if message.startswith("Low SpO2 detected:"):
        value = message.replace(
            "Low SpO2 detected:", ""
        ).strip()

        return f"SpO₂ bajo detectado: {value}"

    # Dynamic pH warning
    if message.startswith("pH outside specification:"):
        value = message.replace(
            "pH outside specification:", ""
        ).strip()

        return f"pH fuera de especificación: {value}"

    # Water warning
    if message == "Water reservoir below safe level.":
        return "Reserva de agua por debajo del nivel seguro."

    # Fallback: leave unknown messages unchanged
    return message


def translate_action(action):
    if action.startswith("Executing response protocol for "):
        scenario_code = (
            action
            .replace("Executing response protocol for ", "")
            .rstrip(".")
        )

        scenario_name = scenario_display_names.get(
            scenario_code,
            scenario_code
        )

        return f"Ejecutando protocolo de respuesta para {scenario_name}."

    return action_display_names.get(action, action)


def translate_event(evento):
    return {
        "system": translate_display(
            evento["system"],
            system_display_names
        ),

        "message": translate_message(
            evento["message"]
        ),

        "action": translate_action(
            evento["action"]
        )
    }

active_phase_name = system_phase_display_names.get(
    st.session_state.system_phase,
    st.session_state.system_phase
)

active_scenario_name = scenario_display_names.get(
    st.session_state.scenario,
    st.session_state.scenario
)

# --------------------------------
# RESILIENCE ARCHITECTURE STATE
# --------------------------------

architecture_state = {
    "reservoir": "OPERATIVO",
    "pump": "OPERATIVA",
    "primary_loop": "ACTIVO",
    "bypass": "EN ESPERA",
    "cultivation": "OPERATIVO"
}

seismic_phase = st.session_state.seismic_phase

if (
    st.session_state.scenario == "SEISMIC"
    and st.session_state.seismic_condition
    == "Cultivation water-loop fault"
):

    if seismic_phase == "FAULT_DETECTED":
        architecture_state["primary_loop"] = "FALLA DETECTADA"
        architecture_state["cultivation"] = "EN EVALUACIÓN"

    elif seismic_phase == "ISOLATED":
        architecture_state["primary_loop"] = "AISLADO"
        architecture_state["cultivation"] = "SERVICIO PROTEGIDO"

    elif seismic_phase == "RECONFIGURED":
        architecture_state["primary_loop"] = "NO DISPONIBLE"
        architecture_state["bypass"] = "ACTIVO"
        architecture_state["cultivation"] = "OPERATIVO"

    elif seismic_phase == "BYPASS_VERIFIED":
        architecture_state["primary_loop"] = "NO DISPONIBLE"
        architecture_state["bypass"] = "ACTIVO — VERIFICADO"
        architecture_state["cultivation"] = "OPERATIVO"

    elif seismic_phase == "RESILIENT_OPERATION":
        architecture_state["primary_loop"] = "NO DISPONIBLE"
        architecture_state["bypass"] = "ACTIVO — REDUNDANCIA"
        architecture_state["cultivation"] = "OPERATIVO"


phase = st.session_state.system_phase

# --------------------------------
# TELEMETRY SEMANTIC STATE
# --------------------------------

def get_telemetry_states(
    bpm,
    spo2,
    co2,
    humedad,
    ph,
    tanque
):
    """
    Resolve the visual semantic state of each telemetry parameter.

    These thresholds mirror the subsystem evaluation logic in
    life_support.py and cultivation.py.
    """

    return {
        "heart_rate": (
            "WARNING"
            if bpm > 120
            else "NOMINAL"
        ),

        "spo2": (
            "CRITICAL"
            if spo2 < 95.0
            else "NOMINAL"
        ),

        "co2": (
            "WARNING"
            if co2 > 1000
            else "NOMINAL"
        ),

        "root_humidity": (
            "WARNING"
            if humedad < 30.0
            else "NOMINAL"
        ),

        "ph": (
            "WARNING"
            if not (5.5 <= ph <= 6.5)
            else "NOMINAL"
        ),

        "water": (
            "WARNING"
            if tanque < 20.0
            else "NOMINAL"
        ),
    }

def status_banner(
    label,
    value,
    state="NOMINAL"
):
    """
    Render a MarsGénesis semantic system-status banner.
    """

    state_class = {
        "NOMINAL": "mg-banner-nominal",
        "STANDBY": "mg-banner-standby",
        "WARNING": "mg-banner-warning",
        "CRITICAL": "mg-banner-critical",
    }.get(
        state,
        "mg-banner-standby"
    )

    banner_html = f"""
    <div class="mg-status-banner {state_class}">

        <div class="mg-status-main">

            <div class="mg-status-dot"></div>

            <div class="mg-status-label">
                {label}
            </div>

        </div>

        <div class="mg-status-value">
            {value}
        </div>

    </div>
    """

    st.html(banner_html)

def telemetry_card(
    system,
    label,
    value,
    state="NOMINAL"
):
    """
    Render a compact MarsGénesis telemetry card.
    """

    state_class = {
        "NOMINAL": "mg-state-nominal",
        "WARNING": "mg-state-warning",
        "CRITICAL": "mg-state-critical",
    }.get(
        state,
        "mg-state-nominal"
    )

    card_html = f"""
    <div class="mg-telemetry-card {state_class}">

        <div>
            <div class="mg-telemetry-system">
                {system}
            </div>

            <div class="mg-telemetry-label">
                {label}
            </div>
        </div>

        <div class="mg-telemetry-reading">

            <div class="mg-telemetry-value">
                {value}
            </div>

            <div class="mg-telemetry-dot"></div>

        </div>

    </div>
    """

    st.html(card_html)

def get_control_phase_state(
    phase,
    seismic_phase=None
):
    """
    Map the current controller phase to the MarsGénesis
    semantic visual vocabulary.
    """

    # Seismic state machine takes precedence while active
    if seismic_phase not in [None, "INACTIVE"]:

        if seismic_phase in [
            "EVENT",
            "FAULT_DETECTED",
        ]:
            return "CRITICAL"

        elif seismic_phase in [
            "SAFE_MODE",
            "ASSESSMENT",
            "RECONFIGURED",
            "BYPASS_VERIFIED",
        ]:
            return "STANDBY"

        elif seismic_phase in [
            "ISOLATED",
            "RESILIENT_OPERATION",
        ]:
            return "WARNING"

        elif seismic_phase == "VERIFIED":
            return "NOMINAL"


    # General autonomous-response phases

    if phase in [
        "RESPONSE ACTIVE",
        "RECOVERING",
    ]:
        return "STANDBY"

    elif phase == "STABILIZED":
        return "NOMINAL"

    elif phase == "NOMINAL":
        return "NOMINAL"

    return "STANDBY"

def system_response(
    system,
    message,
    action=None,
    state="NOMINAL"
):

    state_class = {
        "NOMINAL": "mg-response-nominal",
        "STANDBY": "mg-response-standby",
        "WARNING": "mg-response-warning",
        "CRITICAL": "mg-response-critical",
    }.get(
        state,
        "mg-response-standby"
    )

    state_label = {
        "NOMINAL": "NOMINAL",
        "STANDBY": "EN PROCESO",
        "WARNING": "ADVERTENCIA",
        "CRITICAL": "CRÍTICO",
    }.get(
        state,
        state
    )

    action_html = ""

    if action:
        action_html = f"""
        <div class="mg-response-action">

            <div class="mg-response-action-label">
                Acción Autónoma
            </div>

            <div class="mg-response-action-text">
                {action}
            </div>

        </div>
        """

    response_html = f"""
    <div class="mg-response {state_class}">

        <div class="mg-response-header">

            <div class="mg-response-system">

                <div class="mg-response-dot"></div>

                <div class="mg-response-system-name">
                    {system}
                </div>

            </div>

            <div class="mg-response-state">
                {state_label}
            </div>

        </div>

        <div class="mg-response-message">
            {message}
        </div>

        {action_html}

    </div>
    """

    st.html(response_html)

def control_status(
    cycle,
    scenario,
    phase,
    state="NOMINAL"
):
    """
    Render compact live system context in the fixed control panel.
    """

    state_class = {
        "NOMINAL": "mg-control-nominal",
        "STANDBY": "mg-control-standby",
        "WARNING": "mg-control-warning",
        "CRITICAL": "mg-control-critical",
    }.get(
        state,
        "mg-control-standby"
    )

    status_html = f"""
    <div class="mg-control-status">

        <div class="mg-control-meta-row">
            <div class="mg-control-meta-label">
                Ciclo
            </div>

            <div class="mg-control-meta-value">
                {cycle:02d}
            </div>
        </div>

        <div class="mg-control-meta-row">
            <div class="mg-control-meta-label">
                Escenario
            </div>

            <div class="mg-control-meta-value">
                {scenario}
            </div>
        </div>

        <div class="mg-control-phase {state_class}">

            <div class="mg-control-phase-label">
                Fase del Sistema
            </div>

            <div class="mg-control-phase-state">

                <div class="mg-control-phase-dot"></div>

                <div class="mg-control-phase-value">
                    {phase}
                </div>

            </div>

        </div>

    </div>
    """

    st.html(status_html)

telemetry_states = get_telemetry_states(
    bpm=bpm,
    spo2=spo2,
    co2=co2,
    humedad=humedad,
    ph=ph,
    tanque=tanque
)

def compact_telemetry_chart(
    data,
    column,
    y_min,
    y_max,
    thresholds=None
):

    chart_data = (
        data
        .reset_index()[["Ciclo", column]]
        .rename(columns={column: "Valor"})
    )

    # --------------------------------
    # TELEMETRY TRACE
    # --------------------------------

    line = (
        alt.Chart(chart_data)
        .mark_line(
            color="#A7B4C2",
            strokeWidth=1.8,
            point=alt.OverlayMarkDef(
                color="#D2D5DA",
                filled=True,
                size=28
            )
        )
        .encode(
            x=alt.X(
                "Ciclo:Q",
                title="Ciclo",
                axis=alt.Axis(
                    tickMinStep=1,
                    labelColor="#A7ADB7",
                    titleColor="#A7ADB7",
                    domainColor="#30363D",
                    tickColor="#30363D",
                    gridColor="#30363D",
                    gridOpacity=0.35,
                    labelFontSize=11,
                    titleFontSize=11
                )
            ),

            y=alt.Y(
                "Valor:Q",
                title=None,
                scale=alt.Scale(
                    domain=[y_min, y_max],
                    clamp=True
                ),
                axis=alt.Axis(
                    labelColor="#A7ADB7",
                    domainColor="#30363D",
                    tickColor="#30363D",
                    gridColor="#30363D",
                    gridOpacity=0.35,
                    labelFontSize=11
                )
            ),

            tooltip=[
                alt.Tooltip(
                    "Ciclo:Q",
                    title="Ciclo"
                ),
                alt.Tooltip(
                    "Valor:Q",
                    title="Valor",
                    format=".2f"
                )
            ]
        )
    )

    chart = line

    # --------------------------------
    # SEMANTIC THRESHOLD LINES
    # --------------------------------

    if thresholds:

        threshold_colors = {
            "warning": "#B8892D",
            "critical": "#B84A4A"
        }

        for threshold in thresholds:

            threshold_value = threshold["value"]
            threshold_state = threshold.get(
                "state",
                "warning"
            )

            threshold_color = threshold_colors.get(
                threshold_state,
                "#B8892D"
            )

            rule_data = pd.DataFrame({
                "threshold": [threshold_value]
            })

            rule = (
                alt.Chart(rule_data)
                .mark_rule(
                    color=threshold_color,
                    strokeWidth=1.2,
                    strokeDash=[5, 5],
                    opacity=0.85
                )
                .encode(
                    y="threshold:Q"
                )
            )

            chart = chart + rule

    # --------------------------------
    # MARSGÉNESIS CHART SURFACE
    # --------------------------------

    return (
        chart
        .properties(
            height=160
        )
        .configure_view(
            stroke=None,
            fill="#161B22"
        )
        .configure(
            background="#161B22"
        )
    )

with main_col:
    # --------------------------------
    # BANNERS
    # --------------------------------

    if phase == "RESPONSE ACTIVE":

        status_banner(
            label="Respuesta Autónoma",
            value="ACTIVA",
            state="STANDBY"
        )

    elif phase == "RECOVERING":

        status_banner(
            label="Fase del Sistema",
            value="RECUPERACIÓN",
            state="STANDBY"
        )

    elif phase == "STABILIZED":

        status_banner(
            label="Fase del Sistema",
            value="ESTABILIZADO",
            state="NOMINAL"
        )

        # --------------------------------
    # SEISMIC PHASE BANNERS
    # --------------------------------

    if st.session_state.seismic_phase == "EVENT":

        status_banner(
            label="Evento Sísmico",
            value="DETECTADO",
            state="CRITICAL"
        )

    elif st.session_state.seismic_phase == "SAFE_MODE":

        status_banner(
            label="Modo Seguro",
            value="ACTIVO",
            state="STANDBY"
        )

    elif st.session_state.seismic_phase == "ASSESSMENT":

        status_banner(
            label="Evaluación de Integridad",
            value="EN PROCESO",
            state="STANDBY"
        )

    elif st.session_state.seismic_phase == "VERIFIED":

        status_banner(
            label="Funciones Críticas",
            value="VERIFICADAS",
            state="NOMINAL"
        )

    elif st.session_state.seismic_phase == "FAULT_DETECTED":

        status_banner(
            label="Falla del Sistema",
            value="DETECTADA",
            state="CRITICAL"
        )

    elif st.session_state.seismic_phase == "ISOLATED":

        status_banner(
            label="Circuito Afectado",
            value="AISLADO",
            state="WARNING"
        )

    elif st.session_state.seismic_phase == "RECONFIGURED":

        status_banner(
            label="Red de Suministro",
            value="RECONFIGURADA",
            state="STANDBY"
        )

    elif st.session_state.seismic_phase == "BYPASS_VERIFIED":

        status_banner(
            label="Bypass Redundante",
            value="VERIFICADO",
            state="STANDBY"
        )

    elif st.session_state.seismic_phase == "RESILIENT_OPERATION":

        status_banner(
            label="Operación Resiliente",
            value="ESTABLE",
            state="WARNING"
        )

        if (
            st.session_state.scenario == "SEISMIC"
            and st.session_state.seismic_condition == "Cultivation water-loop fault"
            and st.session_state.seismic_phase in [
                "FAULT_DETECTED",
                "ISOLATED",
                "RECONFIGURED",
                "BYPASS_VERIFIED",
                "RESILIENT_OPERATION",
            ]
        ):

            status_banner(
                label="Estado del Hábitat",
                value="ESTABLE / DEGRADADO",
                state="WARNING"
            )

    elif habitat_status == "CRITICAL":

        status_banner(
            label="Estado del Hábitat",
            value="CRÍTICO",
            state="CRITICAL"
        )

    elif habitat_status == "WARNING":

        status_banner(
            label="Estado del Hábitat",
            value="ADVERTENCIA",
            state="WARNING"
        )

    else:

        status_banner(
            label="Estado del Hábitat",
            value="NOMINAL",
            state="NOMINAL"
        )

    # --------------------------------
    # CURRENT TELEMETRY
    # --------------------------------

    st.divider()

    st.subheader("Telemetría Actual")

    telemetry_row_1 = st.columns(3)
    telemetry_row_2 = st.columns(3)


    # --------------------------------
    # ROW 1 — CREW / ATMOSPHERE
    # --------------------------------

    with telemetry_row_1[0]:
        telemetry_card(
            system="SOPORTE VITAL",
            label="Frecuencia Cardíaca",
            value=f"{bpm:.0f} BPM",
            state=telemetry_states["heart_rate"]
        )


    with telemetry_row_1[1]:
        telemetry_card(
            system="SOPORTE VITAL",
            label="SpO₂ de la Tripulación",
            value=f"{spo2:.1f} %",
            state=telemetry_states["spo2"]
        )


    with telemetry_row_1[2]:
        telemetry_card(
            system="ATMÓSFERA",
            label="CO₂ Atmosférico",
            value=f"{co2:.0f} ppm",
            state=telemetry_states["co2"]
        )


    # --------------------------------
    # ROW 2 — CULTIVATION
    # --------------------------------

    with telemetry_row_2[0]:
        telemetry_card(
            system="CULTIVO",
            label="Humedad Radicular",
            value=f"{humedad:.1f} %",
            state=telemetry_states["root_humidity"]
        )


    with telemetry_row_2[1]:
        telemetry_card(
            system="CULTIVO",
            label="pH de la Solución Nutritiva",
            value=f"{ph:.2f}",
            state=telemetry_states["ph"]
        )


    with telemetry_row_2[2]:
        telemetry_card(
            system="CULTIVO",
            label="Reserva de Agua",
            value=f"{tanque:.1f} %",
            state=telemetry_states["water"]
        )


    # --------------------------------
    # ARCHITECTURE VISUAL STATES
    # --------------------------------

    def architecture_status_class(status):

        if status in [
            "OPERATIVO",
            "OPERATIVA",
            "ACTIVO",
            "ACTIVO — VERIFICADO",
            "ACTIVO — REDUNDANCIA",
            "SERVICIO PROTEGIDO"
        ]:
            return "arch-ok"

        elif status in [
            "FALLA DETECTADA",
            "NO DISPONIBLE"
        ]:
            return "arch-fault"

        elif status in [
            "AISLADO",
            "EN EVALUACIÓN"
        ]:
            return "arch-warning"

        else:
            return "arch-standby"


    # --------------------------------
    # RESILIENCE ARCHITECTURE PANEL
    # --------------------------------

    reservoir_class = architecture_status_class(
    architecture_state["reservoir"]
    )

    pump_class = architecture_status_class(
    architecture_state["pump"]
    )

    primary_class = architecture_status_class(
    architecture_state["primary_loop"]
    )

    bypass_class = architecture_status_class(
    architecture_state["bypass"]
    )

    cultivation_class = architecture_status_class(
    architecture_state["cultivation"]
    )


    # --------------------------------
    # ARCHITECTURE DIAGRAM
    # --------------------------------

    architecture_html = f"""
    <style>

    .architecture-container {{
    width: 100%;
    margin-top: 1rem;
    margin-bottom: 1rem;
    }}

    .architecture-grid {{
    display: grid;

    grid-template-columns:
        1.1fr
        0.45fr
        1.1fr
        0.55fr
        2.2fr
        0.55fr
        1.2fr;

    grid-template-rows:
        auto
        22px
        auto;

    align-items: center;
    column-gap: 10px;
    row-gap: 5px;
    }}

    .arch-node {{
        background: #161B22;

        border: 1px solid #30363D;
        border-left-width: 3px;
        border-radius: 8px;

        padding: 14px 16px;
        min-height: 74px;

        display: flex;
        flex-direction: column;
        justify-content: center;

        box-sizing: border-box;
    }}


    .arch-title {{
        color: #D2D5DA;

        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.035em;

        margin-bottom: 7px;
    }}


    .arch-status {{
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.025em;
    }}


    /* NOMINAL / OPERATIONAL */

    .arch-ok {{
        border-left-color: #1F6F4A;
    }}

    .arch-ok .arch-status {{
        color: #3DDC84;
    }}


    /* CRITICAL / UNAVAILABLE */

    .arch-fault {{
        border-left-color: #8E2A2D;
    }}

    .arch-fault .arch-status {{
        color: #FF5D5D;
    }}


    /* WARNING / DEGRADED */

    .arch-warning {{
        border-left-color: #8A6418;
    }}

    .arch-warning .arch-status {{
        color: #F2B84B;
    }}


    /* STANDBY */

    .arch-standby {{
        border-left-color: #275D8C;
    }}

    .arch-standby .arch-status {{
        color: #69A7E8;
    }}

    .arch-arrow {{
        color: #A7ADB7;

        text-align: center;
        font-size: 1.6rem;
        font-weight: 500;
    }}

    .arch-branch {{
        color: #A7ADB7;

        text-align: center;
        font-size: 1.25rem;
        font-weight: 500;

        line-height: 1.35;
    }}

    .reservoir {{
    grid-column: 1;
    grid-row: 1 / 4;
    }}

    .arrow-reservoir {{
    grid-column: 2;
    grid-row: 1 / 4;
    }}

    .pump {{
    grid-column: 3;
    grid-row: 1 / 4;
    }}

    .branch-left {{
    grid-column: 4;
    grid-row: 1 / 4;
    }}

    .primary {{
    grid-column: 5;
    grid-row: 1;
    }}

    .bypass {{
    grid-column: 5;
    grid-row: 3;
    }}

    .branch-right {{
    grid-column: 6;
    grid-row: 1 / 4;
    }}

    .cultivation {{
    grid-column: 7;
    grid-row: 1 / 4;
    }}

    @media (max-width: 850px) {{

    .architecture-grid {{
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        row-gap: 10px;
    }}

    .reservoir,
    .pump,
    .primary,
    .bypass,
    .cultivation {{
        grid-column: 1;
        grid-row: auto;
    }}

    .arrow-reservoir,
    .branch-left,
    .branch-right {{
        display: none;
    }}
    }}

    </style>


    <div class="architecture-container">

    <div class="architecture-grid">

        <div class="arch-node {reservoir_class} reservoir">
            <div class="arch-title">
                RESERVORIO
            </div>

            <div class="arch-status">
                {architecture_state["reservoir"]}
            </div>
        </div>


        <div class="arch-arrow arrow-reservoir">
            →
        </div>


        <div class="arch-node {pump_class} pump">
            <div class="arch-title">
                BOMBA
            </div>

            <div class="arch-status">
                {architecture_state["pump"]}
            </div>
        </div>


        <div class="arch-branch branch-left">
            ├→
            <br>
            └→
        </div>


        <div class="arch-node {primary_class} primary">
            <div class="arch-title">
                CIRCUITO PRIMARIO
            </div>

            <div class="arch-status">
                {architecture_state["primary_loop"]}
            </div>
        </div>


        <div class="arch-node {bypass_class} bypass">
            <div class="arch-title">
                BYPASS REDUNDANTE
            </div>

            <div class="arch-status">
                {architecture_state["bypass"]}
            </div>
        </div>


        <div class="arch-branch branch-right">
            →┤
            <br>
            →┘
        </div>


        <div class="arch-node {cultivation_class} cultivation">
            <div class="arch-title">
                CULTIVO
            </div>

            <div class="arch-status">
                {architecture_state["cultivation"]}
            </div>
        </div>

    </div>

    </div>
    """

    st.divider()

    st.subheader("Arquitectura de Resiliencia")

    st.caption(
    "Estado dinámico de la red de suministro de agua "
    "del sistema de cultivo."
    )

    st.html(architecture_html)

    st.divider()

    # --------------------------------
    # SYSTEM EVENTS
    # --------------------------------

    st.subheader("Respuesta Actual del Sistema")

    active_events = [
    evento
    for evento in st.session_state.current_events
    if evento["level"] != "NOMINAL"
    ]

    if not active_events:

        system_response(
            system="Sistema de Monitoreo",
            message=(
                "Todos los sistemas monitoreados operan "
                "dentro de los límites establecidos."
            ),
            state="NOMINAL"
        )

    else:

        for evento in active_events:

            evento_display = translate_event(evento)

            if (
                st.session_state.system_phase == "STABLE / DEGRADED"
                and evento["system"] == "Cultivation"
                and tanque < 20
            ):

                response_message = (
                    f"La reserva de agua permanece por debajo "
                    f"del nivel seguro: {tanque:.1f}%."
                )

                response_action = (
                    "Fuga aislada; modo de irrigación "
                    "de reserva activo."
                )

            else:

                response_message = evento_display["message"]
                response_action = evento_display["action"]


            response_state = {
                "CRITICAL": "CRITICAL",
                "WARNING": "WARNING",
                "NOMINAL": "NOMINAL",
            }.get(
                evento["level"],
                "STANDBY"
            )


            system_response(
                system=evento_display["system"],
                message=response_message,
                action=response_action,
                state=response_state
            )


    # --------------------------------
    # TELEMETRY HISTORY
    # --------------------------------

    st.divider()

    with st.expander(
    "Historial de Telemetría",
    expanded=False
    ):

        telemetry_df = pd.DataFrame(
            st.session_state.telemetry_history
        ).copy()

        if not telemetry_df.empty:

            # Use monitoring cycle as the graph index
            telemetry_df["Ciclo"] = range(
                1,
                len(telemetry_df) + 1
            )

            telemetry_df = telemetry_df.set_index("Ciclo")

            graph_col1, graph_col2 = st.columns(2)

            # --------------------------------
            # LIFE SUPPORT
            # --------------------------------

            with graph_col1:

                st.markdown("##### SpO₂ de la Tripulación")
                st.caption("Umbral mínimo: 95%")

                st.altair_chart(
                    compact_telemetry_chart(
                        telemetry_df,
                        "SpO2",
                        92,
                        100,
                        thresholds=[
                            {"value": 95, "state": "critical"}
                        ]
                    ),
                    use_container_width=True
                )

                st.markdown("##### pH de la Solución Nutritiva")
                st.caption("Rango operativo: 5.5–6.5")        

                st.altair_chart(
                    compact_telemetry_chart(
                        telemetry_df,
                        "pH",
                        5.0,
                        6.8,
                        thresholds=[
                            {"value": 5.5, "state": "warning"},
                            {"value": 6.5, "state": "warning"}
                        ]
                    ),
                    use_container_width=True
                )


            # --------------------------------
            # ATMOSPHERE / WATER
            # --------------------------------

            with graph_col2:

                st.markdown("##### CO₂ Atmosférico")
                st.caption("Umbral máximo: 1000 ppm")

                st.altair_chart(
                    compact_telemetry_chart(
                        telemetry_df,
                        "CO2",
                        500,
                        1200,
                        thresholds=[
                            {"value": 1000, "state": "warning"}
                        ]
                    ),
                    use_container_width=True
                )

                st.markdown("##### Reserva de Agua")
                st.caption("Umbral mínimo: 20%")
                st.altair_chart(
                    compact_telemetry_chart(
                        telemetry_df,
                        "Water Reservoir",
                        0,
                        100,
                        thresholds=[
                            {"value": 20, "state": "warning"}
                        ]
                    ),
                    use_container_width=True
                )

        else:

            st.info(
                "Aún no hay datos de telemetría disponibles."
            )


    # --------------------------------
    # EVENT HISTORY
    # --------------------------------

    with st.expander(
        "Historial de Eventos",
        expanded=False
    ):

        if st.session_state.event_history:

            event_html = """
            <div class="mg-event-history">
            """

            for event in st.session_state.event_history:

                # --------------------------------
                # TRANSLATED DISPLAY VALUES
                # --------------------------------

                scenario_name = scenario_display_names.get(
                    event["Scenario"],
                    event["Scenario"]
                )

                event_type = event_type_display_names.get(
                    event["Event Type"],
                    event["Event Type"]
                )

                level = level_display_names.get(
                    event["Level"],
                    event["Level"]
                )

                system = system_display_names.get(
                    event["System"],
                    event["System"]
                )

                message = translate_message(
                    event["Message"]
                )

                action = translate_action(
                    event["Action"]
                )

                # --------------------------------
                # SEMANTIC LEVEL CLASS
                # --------------------------------

                level_class = {
                    "WARNING": "mg-history-warning",
                    "CRITICAL": "mg-history-critical",
                    "ACTION": "mg-history-action",
                    "SUCCESS": "mg-history-success",
                    "NOMINAL": "mg-history-nominal"
                }.get(
                    event["Level"],
                    "mg-history-nominal"
                )

                # --------------------------------
                # TIME
                # --------------------------------

                event_time = event["Time"].strftime(
                    "%H:%M:%S"
                )

                # --------------------------------
                # EVENT RECORD
                # --------------------------------

                event_html += f"""
                <div class="mg-history-event">

                    <div class="mg-history-event-header">

                        <div class="mg-history-event-title">
                            CICLO {event["Cycle"]} · {event_type}
                        </div>

                        <div class="mg-history-event-level {level_class}">
                            {level}
                        </div>

                    </div>

                    <div class="mg-history-event-meta">
                        {system} · {event_time}
                    </div>

                    <div class="mg-history-event-message">
                        {message}
                    </div>

                    <div class="mg-history-event-action">

                        <div class="mg-history-event-action-label">
                            Acción autónoma
                        </div>

                        <div class="mg-history-event-action-text">
                            {action}
                        </div>

                    </div>

                </div>
                """

            event_html += "</div>"

            st.html(event_html)

        else:

            st.success(
                "No se registraron anomalías durante esta sesión."
            )


with control_col:

    control_panel = st.container(
        key="mars_control_panel"
    )

    with control_panel:

        st.subheader("Panel de Control")

        control_phase_state = get_control_phase_state(
            phase=st.session_state.system_phase,
            seismic_phase=st.session_state.seismic_phase
        )

        control_status(
            cycle=st.session_state.cycle_number,
            scenario=active_scenario_name,
            phase=active_phase_name,
            state=control_phase_state
        )

        # Divider removed

        #---------------------------------
        # SCENARIO CONTROL
        #---------------------------------

        st.subheader("Control de Escenarios")

        scenario_options = {
            "Operación Normal": "NORMAL",
            "Evento Sísmico": "SEISMIC",
            "Acumulación de CO₂": "CO2",
            "Bajo Nivel de Oxígeno de la Tripulación": "LOW_OXYGEN",
            "Pérdida de Agua Hidropónica": "WATER_LOSS",
            "Inestabilidad de pH": "PH_INSTABILITY"
        }

        selected_label = st.selectbox(
            "Escenario a insertar:",
            list(scenario_options.keys())
        )

        selected_scenario = scenario_options[selected_label]


        # --------------------------------
        # SEISMIC TEST CONFIGURATION
        # --------------------------------

        if selected_scenario == "SEISMIC":

            seismic_condition_options = {
                "Sin daño en subsistemas": "No subsystem damage",
                "Falla en el circuito de agua del sistema de cultivo":
                    "Cultivation water-loop fault",
            }

            selected_seismic_condition = st.selectbox(
                "Condición de la prueba sísmica:",
                list(seismic_condition_options.keys())
            )

            seismic_condition = seismic_condition_options[
                selected_seismic_condition
            ]

        else:
            seismic_condition = "No subsystem damage"


        # --------------------------------
        # SESSION STATE DEFAULT
        # --------------------------------

        if "seismic_condition" not in st.session_state:
            st.session_state.seismic_condition = "No subsystem damage"


        # --------------------------------
        # INJECT SCENARIO
        # --------------------------------

        if st.button(
            "INSERTAR ESCENARIO",
            use_container_width=True
        ):

            st.session_state.scenario = selected_scenario

            if selected_scenario == "SEISMIC":
                st.session_state.seismic_condition = seismic_condition
            else:
                st.session_state.seismic_condition = "No subsystem damage"

            st.session_state.system_phase = "DEGRADING"
            st.session_state.response_active = False
            st.session_state.response_system = None
            st.session_state.response_cycles = 0

            run_monitoring_cycle()
            st.rerun()

        # --------------------------------
        # MANUAL REFRESH
        # --------------------------------

        if st.button(
            "EJECUTAR SIGUIENTE CICLO",
            use_container_width=True,
            type="primary"
        ):

            run_monitoring_cycle()
            st.rerun()

        if st.button(
            "REINICIAR SIMULACIÓN",
            use_container_width=True
        ):

            st.session_state.telemetry_history = []
            st.session_state.event_history = []
            st.session_state.current_telemetry = None
            st.session_state.current_events = []
            st.session_state.cycle_number = 0

            st.session_state.simulation_state = NOMINAL_STATE.copy()
            st.session_state.scenario = "NORMAL"
            st.session_state.response_active = False
            st.session_state.response_system = None
            st.session_state.system_phase = "NOMINAL"
            st.session_state.seismic_phase = "INACTIVE"
            st.session_state.seismic_timer = 0
            st.session_state.response_cycles = 0
            st.session_state.previous_event_keys = set()

            st.rerun()