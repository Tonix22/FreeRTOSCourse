import threading, queue, time, sys
from collections import deque
import numpy as np
import serial
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# -------- Configura según tu firmware --------
PORT = '/dev/ttyUSB0'
BAUD = 115200
N = 1024            # muestras en ventana (tiempo y FFT)
N_CHANNELS = 2      # cuántos valores imprimes por línea: "v0 v1"
FS_PRINT_HZ = 200.0 # ≈ líneas/seg POR CANAL tras tu decimación (p.ej. 200)
FFT_UPDATE_EVERY = 0.25  # s
# ---------------------------------------------

# Buffers por canal
buffers = [deque([0.0]*N, maxlen=N) for _ in range(N_CHANNELS)]

# ----- Hilo lector de serie (no bloquea la UI) -----
ser = serial.Serial(PORT, BAUD, timeout=0.1)

def serial_reader():
    while True:
        try:
            raw = ser.readline().decode(errors='ignore').strip()
            if not raw:
                continue
            parts = raw.split()
            if len(parts) < N_CHANNELS:
                continue
            vals = [float(x) for x in parts[:N_CHANNELS]]
            for b, v in zip(buffers, vals):
                b.append(v)
        except Exception:
            # no mates el hilo por líneas malas
            pass

t = threading.Thread(target=serial_reader, daemon=True)
t.start()

# ----- Utilidades FFT -----
def compute_fft(y, fs):
    y = np.asarray(y, dtype=float)
    y = y - y.mean()
    w = np.hanning(len(y))
    yw = y * w
    spec = np.fft.rfft(yw)
    cg = w.sum()/len(w)           # coherent gain Hann ~0.5
    mag = np.abs(spec)/(len(y)*cg)
    mag_db = 20*np.log10(mag + 1e-12)
    f = np.fft.rfftfreq(len(y), d=1.0/fs)
    return f, mag_db

# ----- App Dash -----
app = Dash(__name__)
app.layout = html.Div([
    html.H3("ESP32 Serial Plotter (Tiempo + Frecuencia)"),
    html.Div([
        html.Label("Canal para espectro:"),
        dcc.Dropdown(
            id='ch-select',
            options=[{'label': f'Canal {i}', 'value': i} for i in range(N_CHANNELS)],
            value=0, clearable=False, style={'width':'200px'}
        )
    ], style={'marginBottom':'10px'}),

    dcc.Graph(id='time-graph'),
    dcc.Graph(id='freq-graph'),

    dcc.Interval(id='timer', interval=1000/30, n_intervals=0),     # ~30 FPS tiempo
    dcc.Interval(id='fft-timer', interval=int(FFT_UPDATE_EVERY*1000), n_intervals=0)
])

@app.callback(Output('time-graph','figure'), Input('timer','n_intervals'))
def update_time(_):
    x = np.arange(N)/FS_PRINT_HZ
    data = []
    for i, b in enumerate(buffers):
        y = np.array(b, dtype=float)
        data.append(go.Scatter(x=x, y=y, mode='lines', name=f'Ch {i}'))
    fig = go.Figure(data=data)
    fig.update_layout(margin=dict(l=40,r=10,t=30,b=40))
    fig.update_xaxes(title="Tiempo (s)")
    fig.update_yaxes(title="Valor (códigos ADC)")
    return fig

@app.callback(Output('freq-graph','figure'),
              [Input('fft-timer','n_intervals'), Input('ch-select','value')])
def update_fft(_, ch):
    y = np.array(buffers[ch], dtype=float)
    f, mag_db = compute_fft(y, FS_PRINT_HZ)
    peak_idx = int(np.argmax(mag_db))
    peak_f = float(f[peak_idx]); peak_db = float(mag_db[peak_idx])

    fig = go.Figure(data=[go.Scatter(x=f, y=mag_db, mode='lines', name=f'Ch {ch}')])
    fig.update_layout(
        margin=dict(l=40,r=10,t=30,b=40),
        title=f"Espectro (Hann) — pico ≈ {peak_f:.1f} Hz ({peak_db:.1f} dB rel)"
    )
    fig.update_xaxes(title="Frecuencia (Hz)", range=[0, FS_PRINT_HZ/2])
    fig.update_yaxes(title="Magnitud (dB rel)", range=[-120, 0])
    return fig

if __name__ == "__main__":
    # choose a free port if 8050 is busy
    HOST = "127.0.0.1"
    PORT = 8050

    # Dash 3+ uses app.run(); Dash 2.x uses app.run_server()
    if hasattr(app, "run") and callable(getattr(app, "run")):
        app.run(debug=False, host=HOST, port=PORT)          # Dash >= 3
    else:
        app.run_server(debug=False, host=HOST, port=PORT)    # Dash 2.x fallback
