from uuid import uuid4

from weapons import Bullet


def test_bullet_target():
    values = [
        # right down quadrant (x2 > x1 and y2 > y1)
        {
            "position": (4, 3),
            "target": (6, 5),
            "test": [
                (5, 4),
                (7, 6),
                (8, 7),
                (9, 8)
            ]
        },
        {
            "position": (212, 110),
            "target": (254, 381),
            "test": [
                (230, 1583 / 7),
                (252, 7730 / 21),
                (414, 29681 / 21)
            ]
        },
        # left down quadrant (x2 < x1 and y2 > y1)
        {
            "position": (4, 5),
            "target": (1, 8),
            "test": [
                (2, 7),
                (3, 6),
                (0, 9)
            ]
        },
        {
            "position": (369, 220),
            "target": (105, 250),
            "test": [
                (160, 975 / 4),
                (256, 10245 / 44),
                (389, 2395 / 11)
            ]
        },
        # right up quadrant (x2 > x1 and y2 < y1)
        {
            "position": (251, 289),
            "target": (499, 101),
            "test": [
                (321, 7314 / 31),
                (388, 11479 / 62),
                (522, 5181 / 62)
            ]
        },
        {
            "position": (16, 332),
            "target": (19, 101),
            "test": [
                (17, 255),
                (15, 409),
                (20, 24),
                (22, -130)
            ]
        },
        # left up quadrant (x2 < x1 and y2 - y1)
        {
            "position": (222, 222),
            "target": (101, 62),
            "test": [
                (130, 12142 / 121),
                (180, 20142 / 121),
                (230, 28142 / 121),
                (60, 942 / 121),
            ]
        }
    ]
    index = 0
    for value in values:
        print(f"--- Testing #{index} ---")
        index += 1
        bullet = Bullet(uuid4(), 1, 1, "bullet.png", x=value["position"][0], y=value["position"][1], height=4)
        bullet.target(x=value["target"][0], y=value["target"][1])
        fx = bullet.fx
        fy = bullet.fy
        for test in value["test"]:
            y = round(fx(test[0]), 3)
            x = round(fy(test[1]), 3)
            print(
                f"Testing fx({test[0]}) = {y} ({round(test[1], 3)}) / Testing fy({test[1]}) = {x} ({round(test[0], 3)})"
            )
            assert y == round(test[1], 3), f"fx({test[0]}) = {round(test[1], 3)}"
            assert x == round(test[0], 3), f"fy({test[1]}) = {round(test[0], 3)}"


if __name__ == "__main__":
    test_bullet_target()
    print("--- All tests passed ---")
