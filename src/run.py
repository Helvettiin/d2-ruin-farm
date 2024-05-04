import time
from pathlib import Path
from loguru import logger

X_SIMILARITY_CHECK_INTERVAL = 4
BOSS_HP_BAR_CHECK_INTERVAL = 0.5


def run():
    from pydirectinput import press
    from screenshot import (
        get_x_similarity,
        get_boss_hp_bar_mask_ratio,
        get_finish_hp_bar_mask_ratio,
        get_normal_hp_bar_mask_ratio,
    )
    from directx import (
        kick_boss_by_indebted_kindess,
        start_next_round,
        refresh_checkpoint,
        hide_indebted_kindess,
    )
    from settings import base_settings, monitor_settings

    logger.add("./logs/d2-ruin-farm_{time}.log", level=base_settings.log_level)
    logger.info(base_settings)
    logger.info(monitor_settings)

    start_count = 0
    finish_count = 0
    success_count = 0
    continuous_fail_count = 0
    need_refresh_checkpoint = False

    logger.info("program start")

    if base_settings.debug:
        logger.info("open debug")
        Path("./debug").mkdir(exist_ok=True)

    time.sleep(2)

    while True:
        while True:
            x_similarity = get_x_similarity()
            if x_similarity > 0.9:
                logger.info("x is already")
                break
            time.sleep(X_SIMILARITY_CHECK_INTERVAL)

        if continuous_fail_count >= 30:
            logger.info("Failed more than 30 times,reenter")
            start_next_round()
            need_refresh_checkpoint = True
            continuous_fail_count = 0
            continue

        if need_refresh_checkpoint:
            refresh_checkpoint()
            need_refresh_checkpoint = False
            continue

        logger.info(
            f"start_count: {start_count}, finish_count: {finish_count}, success_count: {success_count}"
        )
        start_count += 1

        kick_boss_by_indebted_kindess()
        time.sleep(0.1)

        hp_bar_mask_ratio = get_finish_hp_bar_mask_ratio()

        if not hp_bar_mask_ratio >= 0.8:
            continuous_fail_count += 1
            logger.info("Sensor shield not detected on player health bar，retry")

            press(base_settings.职业技能按键)
            time.sleep(1.5)
            press(base_settings.未充能近战按键)
            time.sleep(10)

            continue

        finish_count += 1
        logger.info("Detection successful")

        start_time = time.monotonic()

        # wait boss die
        time.sleep(2)
        hide_indebted_kindess()

        while True:
            if time.monotonic() - start_time >= 25:
                continuous_fail_count += 1
                logger.info("Timeout waiting for boss health bar to disappear，Retry")

                press(base_settings.未充能近战按键)
                time.sleep(10)

                break

            boss_hp_bar_mask_ratio = get_boss_hp_bar_mask_ratio()

            # If the boss's health bar disappears, check the player's health bar.
            if boss_hp_bar_mask_ratio <= 0.1:
                logger.info("boss血条已消失")

                normal_hp_bar_mask_ratio = get_normal_hp_bar_mask_ratio()

                # If the player's health bar is detected again, it means success.
                if normal_hp_bar_mask_ratio >= 0.8:
                    success_count += 1
                    continuous_fail_count = 0
                    need_refresh_checkpoint = True
                    logger.success("The player's health bar has been detected，successful")

                    time.sleep(2)
                    start_next_round()

                    break
                # If the player's health bar is not detected, it means failure.
                else:
                    logger.info("Player's health bar not detected，Retry")
                    continuous_fail_count += 1
                    break

            time.sleep(BOSS_HP_BAR_CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        ...
    except Exception as e:
        import sys

        logger.exception(e)
        sys.exit(1)
