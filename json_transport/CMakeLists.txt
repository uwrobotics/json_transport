cmake_minimum_required(VERSION 3.5)
project(json_transport)

# Set C++ standard (ROS 2 defaults to C++14, but we ensure it)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optionally add compile flags
add_compile_options(-Wall -Werror)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(json_msgs REQUIRED)
find_package(nlohmann_json REQUIRED)

# Create an INTERFACE library target for this header-only package.
add_library(${PROJECT_NAME} INTERFACE)
target_include_directories(${PROJECT_NAME} INTERFACE
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# Export dependencies so that downstream packages linking to json_transport get these includes.
ament_export_dependencies(rclcpp json_msgs nlohmann_json)
ament_export_include_directories(include)

# Install the INTERFACE target with an export name
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}Targets
  INCLUDES DESTINATION include
)

# Export the installed targets for downstream usage
ament_export_targets(${PROJECT_NAME}Targets)

# Install public header files (the header files should be placed in include/json_transport/)
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
)

# Install extra files (e.g. pip requirements)
install(FILES requirements.txt
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  # Linting (requires ament_lint_auto)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  # --- C++ Tests ---
  # Test executable from test/talker.cpp
  ament_add_gtest(talker_cpp test/talker.cpp)
  if(TARGET talker_cpp)
    target_link_libraries(talker_cpp
      rclcpp
      nlohmann_json::nlohmann_json
    )
  endif()

  # Test executable from test/test_listener.cpp
  ament_add_gtest(test_listener_cpp test/test_listener.cpp)
  if(TARGET test_listener_cpp)
    target_link_libraries(test_listener_cpp
      rclcpp
      nlohmann_json::nlohmann_json
    )
  endif()

  # --- Python Tests ---
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(talker_py test/talker_py)
  ament_add_pytest_test(test_listener_py test/test_listener_py)
  ament_add_pytest_test(test_packed_json test/test_packed_json.py)
endif()

ament_package()
