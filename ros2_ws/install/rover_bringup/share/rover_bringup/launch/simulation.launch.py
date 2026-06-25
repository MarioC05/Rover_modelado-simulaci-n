from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():


    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rover_bringup'),
                'launch',
                'robot_gazebo.launch.py'
            ])
        ),

        launch_arguments={'world_name': 'urjc_excavation_msr'}.items()
    )

  
    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rover_moveit_config'),
                'launch',
                'move_group.launch.py' 
            ])
        )
    )


    controllers_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('rover_bringup'),
                'launch',
                'robot_controllers.launch.py'
            ])
        )
    )

   
    delay_moveit = TimerAction(
        period=12.0,
        actions=[moveit_launch]
    )

    
    delay_controllers = TimerAction(
        period=12.0,
        actions=[controllers_launch]
    )

    # Devolvemos la descripción del lanzamiento
    return LaunchDescription([
        gazebo_launch,       # Arranca de inmediato (Tiempo 0s)
        delay_moveit,        # Arranca tras 8 segundos
        delay_controllers    # Arranca tras 12 segundos
    ])