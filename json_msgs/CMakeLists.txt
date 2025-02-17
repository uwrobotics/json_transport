cmake_minimum_required(VERSION 3.5)
project(json_msgs)

# Find ament and message generation dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# List the message files
set(msg_files
  "msg/Json.msg"
)

# Generate interfaces (messages, services, actions)
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
)

# Export the dependency on the runtime package for generated messages.
ament_export_dependencies(rosidl_default_runtime)

ament_package()
