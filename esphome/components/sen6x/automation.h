#pragma once

#include "esphome/core/component.h"
#include "esphome/core/automation.h"
#include "sen6x.h"

namespace esphome {
namespace sen6x {

template<typename... Ts> class StartFanCleaningAction : public Action<Ts...>, public Parented<Sen6xComponent> {
 public:
  void play(const Ts &...x) override { this->parent_->start_fan_cleaning(); }
};

}  // namespace sen6x
}  // namespace esphome
