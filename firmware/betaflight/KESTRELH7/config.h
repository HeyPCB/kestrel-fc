/*
 * Kestrel H7 - Betaflight unified target (config.h for the betaflight/config repository, 4.5+).
 *
 * Every pin below is the net the board's brief puts on that MCU pin (design/make_brief.py,
 * MCU_PINS), named from the KiCad 10 MCU_ST_STM32H7:STM32H743VITx symbol. The motor, LED-strip, UART,
 * I2C1, SPI1, SPI4 and ADC pins are the ones MATEKH743 ships with (configs/MTKS/MATEKH743/config.h,
 * read 2026-10-05), so their timer and DMA assignments below are that target's, unchanged.
 *
 * Not in Betaflight: the BMI088 (gyro 2, SPI4, CS PE11 / PE10) has no Betaflight driver; it is the
 * second IMU for INAV and ArduPilot. Betaflight flies on the ICM-20602 alone.
 *
 * Build:  make CONFIG=KESTRELH7   (with this directory copied to configs/KESTRELH7 of betaflight/config)
 */

#pragma once

#define FC_TARGET_MCU     STM32H743

#define BOARD_NAME        KESTRELH7
#define MANUFACTURER_ID   HYPB

#define USE_ACC
#define USE_ACC_SPI_MPU6500         // ICM-20602 is read by the MPU6500 driver family
#define USE_GYRO
#define USE_GYRO_SPI_MPU6500
#define USE_BARO
#define USE_BARO_MS5611           // I2C1 at 0x77
#define USE_MAG
#define USE_MAG_LIS3MDL             // Kestrel GPS board's compass, I2C1 at 0x1E
#define USE_FLASH
#define USE_FLASH_W25Q128FV
#define USE_GPS

#define BEEPER_PIN           PD15
#define MOTOR1_PIN           PB0
#define MOTOR2_PIN           PB1
#define MOTOR3_PIN           PA0
#define MOTOR4_PIN           PA1
#define MOTOR5_PIN           PA2
#define MOTOR6_PIN           PA3
#define MOTOR7_PIN           PD12
#define MOTOR8_PIN           PD13
#define LED_STRIP_PIN        PA8
#define UART1_TX_PIN         PA9
#define UART2_TX_PIN         PD5
#define UART3_TX_PIN         PD8
#define UART6_TX_PIN         PC6
#define UART7_TX_PIN         PE8
#define UART1_RX_PIN         PA10
#define UART2_RX_PIN         PD6
#define UART3_RX_PIN         PD9
#define UART4_RX_PIN         PB8      // ESC telemetry in (the 4-in-1's TLM wire)
#define UART6_RX_PIN         PC7
#define UART7_RX_PIN         PE7
#define I2C1_SCL_PIN         PB6
#define I2C1_SDA_PIN         PB7
#define LED0_PIN             PE3
#define LED1_PIN             PE4
#define SPI1_SCK_PIN         PA5
#define SPI3_SCK_PIN         PC10
#define SPI4_SCK_PIN         PE12
#define SPI1_SDI_PIN         PA6
#define SPI3_SDI_PIN         PC11
#define SPI4_SDI_PIN         PE13
#define SPI1_SDO_PIN         PD7
#define SPI3_SDO_PIN         PC12
#define SPI4_SDO_PIN         PE14
#define ADC_VBAT_PIN         PC0
#define ADC_CURR_PIN         PC1
#define PINIO1_PIN           PE2      // high switches the 10 V VTX rail off
#define FLASH_CS_PIN         PA15
#define GYRO_1_EXTI_PIN      PB2
#define GYRO_1_CS_PIN        PC15

#define TIMER_PIN_MAPPING \
    TIMER_PIN_MAP( 0, PB0 , 2,  0) \
    TIMER_PIN_MAP( 1, PB1 , 2,  1) \
    TIMER_PIN_MAP( 2, PA0 , 2,  2) \
    TIMER_PIN_MAP( 3, PA1 , 2,  3) \
    TIMER_PIN_MAP( 4, PA2 , 2,  4) \
    TIMER_PIN_MAP( 5, PA3 , 2,  5) \
    TIMER_PIN_MAP( 6, PD12, 1,  6) \
    TIMER_PIN_MAP( 7, PD13, 1,  7) \
    TIMER_PIN_MAP( 8, PA8 , 1,  8)

#define ADC1_DMA_OPT        9
#define TIMUP3_DMA_OPT      11
#define TIMUP4_DMA_OPT      12
#define TIMUP5_DMA_OPT      13

#define BARO_I2C_INSTANCE   I2CDEV_1
#define MAG_I2C_INSTANCE    I2CDEV_1

#define DEFAULT_RX_FEATURE  FEATURE_RX_SERIAL
#define SERIALRX_UART       SERIAL_PORT_UART7      // the RX port: an ELRS receiver, CRSF

#define DEFAULT_BLACKBOX_DEVICE      BLACKBOX_DEVICE_FLASH
#define DEFAULT_CURRENT_METER_SOURCE CURRENT_METER_ADC
#define DEFAULT_VOLTAGE_METER_SOURCE VOLTAGE_METER_ADC
#define DEFAULT_CURRENT_METER_SCALE  125   // Kestrel 4in1: INA180A2 x 0.25 mOhm = 12.5 mV/A
#define DEFAULT_VOLTAGE_METER_SCALE  110   // 10k / 1k divider
#define BEEPER_INVERTED                    // an AO3400A low-side switch: the pin high sounds it

#define FLASH_SPI_INSTANCE  SPI3
#define PINIO1_BOX          40
#define GYRO_1_SPI_INSTANCE SPI1
// The ICM-20602 sits on the bottom face (its Z axis points down). Derived from the footprint, not yet
// measured on a board: check the Configurator's Setup tab before the first flight and correct with
// "set gyro_1_sensor_align" if the model does not follow the quad.
#define GYRO_1_ALIGN        CW0_DEG_FLIP
