| Argument         | Type           | Default                                            | Description                                                                                                                                                                                            |
| ---------------- | -------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `region`         | `list`         | `[(20, 400), (1080, 400), (1080, 360), (20, 360)]` | Defines the region points for object counting, queue monitoring, trackzone or speed estimation. The points are defined as coordinates forming a polygonal area for analysis.                           |
| `show_in`        | `bool`         | `True`                                             | Indicates whether to display objects that are counted as entering the defined region. Essential for real-world analytics, such as monitoring ingress trends.                                           |
| `show_out`       | `bool`         | `True`                                             | Indicates whether to display objects that are counted as exiting the defined region. Useful for applications requiring egress tracking and analytics.                                                  |
| `colormap`       | `int or tuple` | `COLORMAP_PARULA`                                  | Specifies the OpenCV-supported colormap for heatmap visualization. Default is `COLORMAP_PARULA`, but other colormaps can be used for different visualization preferences.                              |
| `up_angle`       | `float`        | `145.0`                                            | Angle threshold for detecting the "up" position in workouts monitoring. Can be adjusted based on the position of keypoints for different exercises.                                                    |
| `down_angle`     | `float`        | `90.0`                                             | Angle threshold for detecting the "down" position in workouts monitoring. Adjust this based on keypoint positions for specific exercises.                                                              |
| `kpts`           | `list`         | `[6, 8, 10]`                                       | List of keypoints used for monitoring workouts. These keypoints correspond to body joints or parts, such as shoulders, elbows, and wrists, for exercises like push-ups, pull-ups, squats, ab-workouts. |
| `analytics_type` | `str`          | `line`                                             | Specifies the type of analytics visualization to generate. Options include `"line"`, `"pie"`, `"bar"`, or `"area"`. The default is `"line"` for trend visualization.                                   |
| `json_file`      | `str`          | `None`                                             | Path to the JSON file defining regions for parking systems or similar applications. Enables flexible configuration of analysis areas.                                                                  |
| `records`        | `int`          | `5`                                                | Total detections count that triggers an automated email notification about unusual activity.                                                                                                           |