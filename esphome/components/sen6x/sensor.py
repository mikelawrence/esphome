from esphome import automation
import esphome.codegen as cg
from esphome.components import i2c, sensirion_common, sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ALTITUDE_COMPENSATION,
    CONF_AMBIENT_PRESSURE_COMPENSATION_SOURCE,
    CONF_AUTOMATIC_SELF_CALIBRATION,
    CONF_CO2,
    CONF_HUMIDITY,
    CONF_ID,
    CONF_NOX,
    CONF_PM_1_0,
    CONF_PM_2_5,
    CONF_PM_4_0,
    CONF_PM_10_0,
    CONF_TEMPERATURE,
    CONF_TYPE,
    CONF_VOC,
    DEVICE_CLASS_AQI,
    DEVICE_CLASS_CARBON_DIOXIDE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PM1,
    DEVICE_CLASS_PM10,
    DEVICE_CLASS_PM25,
    DEVICE_CLASS_TEMPERATURE,
    ICON_CHEMICAL_WEAPON,
    ICON_MOLECULE_CO2,
    ICON_RADIATOR,
    ICON_THERMOMETER,
    ICON_WATER_PERCENT,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_MICROGRAMS_PER_CUBIC_METER,
    UNIT_PARTS_PER_BILLION,
    UNIT_PARTS_PER_MILLION,
    UNIT_PERCENT,
)

CODEOWNERS = ["@mikelawrence"]
DEPENDENCIES = ["i2c"]
AUTO_LOAD = ["sensirion_common"]

sen6x_ns = cg.esphome_ns.namespace("sen6x")
Sen6xComponent = sen6x_ns.class_(
    "Sen6xComponent", cg.PollingComponent, sensirion_common.SensirionI2CDevice
)
Sen6xType = sen6x_ns.enum("Sen6xType", is_class=True)

CONF_K = "k"
CONF_HCHO = "hcho"
ICON_MOLECULE = "mdi:molecule"
CONF_P = "p"
CONF_SLOT = "slot"
CONF_STORE_ALGORITHM_STATE = "store_algorithm_state"
CONF_T1 = "t1"
CONF_T2 = "t2"
CONF_TEMPERATURE_ACCELERATION = "temperature_acceleration"

# Actions
StartFanCleaningAction = sen6x_ns.class_("StartFanCleaningAction", automation.Action)
ActivateHeaterAction = sen6x_ns.class_("ActivateHeaterAction", automation.Action)

BASE_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Sen6xComponent),
            cv.Optional(CONF_PM_1_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PM1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_2_5): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PM25,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_4_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=2,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PM_10_0): sensor.sensor_schema(
                unit_of_measurement=UNIT_MICROGRAMS_PER_CUBIC_METER,
                icon=ICON_CHEMICAL_WEAPON,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PM10,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                icon=ICON_THERMOMETER,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                icon=ICON_WATER_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("60s"))
    .extend(i2c.i2c_device_schema(0x6B))
)

CO2_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_CO2): sensor.sensor_schema(
            unit_of_measurement=UNIT_PARTS_PER_MILLION,
            icon=ICON_MOLECULE_CO2,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_CARBON_DIOXIDE,
            state_class=STATE_CLASS_MEASUREMENT,
        ).extend(
            cv.Schema(
                {
                    cv.Optional(
                        CONF_AUTOMATIC_SELF_CALIBRATION, default=True
                    ): cv.boolean,
                    cv.Optional(CONF_ALTITUDE_COMPENSATION): cv.int_range(
                        min=0, max=3000
                    ),
                    cv.Optional(CONF_AMBIENT_PRESSURE_COMPENSATION_SOURCE): cv.use_id(
                        sensor.Sensor
                    ),
                }
            )
        ),
    }
)

VOC_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_VOC): sensor.sensor_schema(
            icon=ICON_RADIATOR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_AQI,
            state_class=STATE_CLASS_MEASUREMENT,
        ).extend(
            cv.Schema(
                {
                    cv.Optional(CONF_STORE_ALGORITHM_STATE): cv.boolean,
                }
            )
        ),
    }
)

NOX_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_NOX): sensor.sensor_schema(
            icon=ICON_RADIATOR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_AQI,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

HCHO_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_HCHO): sensor.sensor_schema(
            unit_of_measurement=UNIT_PARTS_PER_BILLION,
            icon=ICON_MOLECULE,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

SEN65_SCHEMA = BASE_SCHEMA.extend(VOC_SCHEMA).extend(NOX_SCHEMA)

CONFIG_SCHEMA = cv.Schema(
    cv.typed_schema(
        {
            "SEN62": BASE_SCHEMA,
            "SEN63C": BASE_SCHEMA.extend(CO2_SCHEMA),
            "SEN65": SEN65_SCHEMA,
            "SEN66": SEN65_SCHEMA.extend(CO2_SCHEMA),
            "SEN68": SEN65_SCHEMA.extend(HCHO_SCHEMA),
            "SEN69C": SEN65_SCHEMA.extend(CO2_SCHEMA).extend(HCHO_SCHEMA),
        },
        upper=True,
    ),
)

SENSOR_MAP = {
    CONF_PM_1_0: "set_pm_1_0_sensor",
    CONF_PM_2_5: "set_pm_2_5_sensor",
    CONF_PM_4_0: "set_pm_4_0_sensor",
    CONF_PM_10_0: "set_pm_10_0_sensor",
    CONF_VOC: "set_voc_sensor",
    CONF_NOX: "set_nox_sensor",
    CONF_TEMPERATURE: "set_temperature_sensor",
    CONF_HUMIDITY: "set_humidity_sensor",
    CONF_CO2: "set_co2_sensor",
    CONF_HCHO: "set_hcho_sensor",
}

CO2_SETTING_MAP = {
    CONF_AUTOMATIC_SELF_CALIBRATION: "set_automatic_self_calibrate",
    CONF_ALTITUDE_COMPENSATION: "set_altitude_compensation",
}

FINAL_VALIDATE_SCHEMA = i2c.final_validate_device_schema(
    "sen6x", max_frequency="100kHz"
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    cg.add(var.set_type(getattr(Sen6xType, config[CONF_TYPE])))
    for key, funcName in SENSOR_MAP.items():
        if cfg := config.get(key):
            sens = await sensor.new_sensor(cfg)
            cg.add(getattr(var, funcName)(sens))
    if cfg := config.get(CONF_VOC, {}).get(CONF_STORE_ALGORITHM_STATE):
        cg.add(var.set_store_voc_algorithm_state(cfg))
    if cfg := config.get(CONF_CO2):
        for key, funcName in CO2_SETTING_MAP.items():
            if setting := config.get(key):
                cg.add(getattr(var, funcName)(setting))
        if source := cfg.get(CONF_AMBIENT_PRESSURE_COMPENSATION_SOURCE):
            sens = await cg.get_variable(source)
            cg.add(var.set_ambient_pressure_compensation_source(sens))
