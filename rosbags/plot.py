from pathlib import Path
from rosbags.highlevel import AnyReader
import matplotlib.pyplot as plt

# ========= CONFIGURACIÓN =========

BAG_PATH = "green+10m"

WHEEL_JOINTS = [
    'wheel1_link_joint',
    'wheel2_link_joint',
    'wheel3_link_joint',
    'wheel4_link_joint',
    'wheel5_link_joint',
    'wheel6_link_joint'
]

# ========= DATOS =========

wheel_time = []
wheel_positions = {joint: [] for joint in WHEEL_JOINTS}

imu_time = []
acc_x = []
acc_y = []
acc_z = []

# ========= LECTURA DEL BAG =========

with AnyReader([Path(BAG_PATH)]) as reader:

    start_time = None

    for connection, timestamp, rawdata in reader.messages():

        if start_time is None:
            start_time = timestamp

        t = (timestamp - start_time) * 1e-9  # ns -> s

        msg = reader.deserialize(rawdata, connection.msgtype)

        # --------------------------
        # JOINT STATES
        # --------------------------
        if connection.topic == "/joint_states":

            wheel_time.append(t)

            pos_dict = dict(zip(msg.name, msg.position))

            for joint in WHEEL_JOINTS:

                if joint in pos_dict:
                    wheel_positions[joint].append(pos_dict[joint])
                else:
                    wheel_positions[joint].append(float('nan'))

        # --------------------------
        # IMU
        # --------------------------
        elif connection.topic == "/imu/data":

            imu_time.append(t)

            acc_x.append(msg.linear_acceleration.x)
            acc_y.append(msg.linear_acceleration.y)
            acc_z.append(msg.linear_acceleration.z)

# ========= GRÁFICA 1 =========

plt.figure(figsize=(12, 6))

for joint in WHEEL_JOINTS:
    plt.plot(
        wheel_time,
        wheel_positions[joint],
        label=joint
    )

plt.title("Posición de ruedas vs tiempo")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posición [rad]")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("ruedas_vs_tiempo.png", dpi=300)

# ========= GRÁFICA 2 =========

plt.figure(figsize=(12, 6))

plt.plot(imu_time, acc_x, label='ax')
plt.plot(imu_time, acc_y, label='ay')
plt.plot(imu_time, acc_z, label='az')

plt.title("Aceleración IMU vs tiempo")
plt.xlabel("Tiempo [s]")
plt.ylabel("Aceleración [m/s²]")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("imu_vs_tiempo.png", dpi=300)

plt.show()

print("Gráficas guardadas:")
print("  ruedas_vs_tiempo.png")
print("  imu_vs_tiempo.png")