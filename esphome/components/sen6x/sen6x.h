#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/sensirion_common/i2c_sensirion.h"
#include "esphome/core/application.h"
#include "esphome/core/preferences.h"
#include <algorithm>

namespace esphome {
namespace sen6x {

enum class SetupStates : uint8_t {
  SM_START,
  SM_START_1,
  SM_GET_SN,
  SM_GET_SN_1,
  SM_GET_PN,
  SM_GET_FW,
  SM_SET_VOCB,
  SM_SET_CO2ASC,
  SM_SET_CO2AC,
  SM_SENSOR_CHECK,
  SM_START_MEAS,
  SM_DONE
};

enum class Sen6xType : uint8_t { SEN62, SEN63C, SEN65, SEN66, SEN68, SEN69C, UNKNOWN };

struct GasTuning {
  uint16_t index_offset;
  uint16_t learning_time_offset_hours;
  uint16_t learning_time_gain_hours;
  uint16_t gating_max_duration_minutes;
  uint16_t std_initial;
  uint16_t gain_factor;
};

// Shortest time interval of 2H (in milliseconds) for storing baseline values.
// Prevents wear of the flash because of too many write operations
static const uint32_t SHORTEST_BASELINE_STORE_INTERVAL = 2 * 60 * 60 * 1000;

class Sen6xComponent : public PollingComponent, public sensirion_common::SensirionI2CDevice {
  SUB_SENSOR(pm_1_0)
  SUB_SENSOR(pm_2_5)
  SUB_SENSOR(pm_4_0)
  SUB_SENSOR(pm_10_0)
  SUB_SENSOR(temperature)
  SUB_SENSOR(humidity)
  SUB_SENSOR(voc)
  SUB_SENSOR(nox)
  SUB_SENSOR(co2)
  SUB_SENSOR(hcho)
  SUB_SENSOR(co2_ambient_pressure_source)

 public:
  void setup() override;
  void dump_config() override;
  void update() override;
  void set_store_voc_algorithm_state(bool store_voc_algorithm_state) {
    this->store_voc_algorithm_state_ = store_voc_algorithm_state;
  }
  void set_type(Sen6xType type) { this->type_ = type; }
  void set_automatic_self_calibration(bool value) { this->auto_self_calibration_ = value; }
  void set_altitude_compensation(uint16_t altitude) { this->altitude_compensation_ = altitude; }
  void set_ambient_pressure_compensation_source(sensor::Sensor *pressure) {
    this->ambient_pressure_compensation_source_ = pressure;
  }
  void set_ambient_pressure_compensation(uint16_t pressure_in_hpa);
  void start_fan_cleaning();
  bool busy() { return this->busy_ || this->updating_; };

 protected:
  void internal_setup_(SetupStates state);
  bool has_co2_() const;
  bool start_measurements_();
  bool stop_measurements_();
  bool write_ambient_pressure_compensation_(uint16_t pressure_in_hpa);

  char serial_number_[17] = "UNKNOWN";
  uint16_t voc_algorithm_state_[4]{0};
  sensor::Sensor *ambient_pressure_compensation_source_;
  uint32_t voc_algorithm_time_;
  uint16_t ambient_pressure_compensation_{0};
  uint8_t firmware_major_{0xFF};
  uint8_t firmware_minor_{0xFF};
  bool initialized_{false};
  bool running_{false};
  bool updating_{false};
  bool busy_{false};
  bool voc_algorithm_error_{false};

  optional<Sen6xType> type_;
  optional<bool> auto_self_calibration_;
  optional<uint16_t> altitude_compensation_;
  optional<bool> store_voc_algorithm_state_;

  ESPPreferenceObject pref_;
};
}  // namespace sen6x
}  // namespace esphome
