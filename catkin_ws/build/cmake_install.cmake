# Install script for directory: /home/ubuntu/catkin_ws/src

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/home/ubuntu/catkin_ws/install")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
        file(MAKE_DIRECTORY "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}")
      endif()
      if (NOT EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin")
        file(WRITE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/.catkin" "")
      endif()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/_setup_util.py")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE PROGRAM FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/_setup_util.py")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/env.sh")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE PROGRAM FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/env.sh")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/setup.bash")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE FILE FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/setup.bash")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/setup.sh")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE FILE FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/setup.sh")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/setup.zsh")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE FILE FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/setup.zsh")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CPACK_ABSOLUTE_DESTINATION_FILES
   "/home/ubuntu/catkin_ws/install/.rosinstall")
FILE(INSTALL DESTINATION "/home/ubuntu/catkin_ws/install" TYPE FILE FILES "/home/ubuntu/catkin_ws/build/catkin_generated/installspace/.rosinstall")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/etc/catkin/profile.d" TYPE FILE FILES "/opt/ros/hydro/share/catkin/cmake/env-hooks/05.catkin_make.bash")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/etc/catkin/profile.d" TYPE FILE FILES "/opt/ros/hydro/share/catkin/cmake/env-hooks/05.catkin_make_isolated.bash")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  INCLUDE("/home/ubuntu/catkin_ws/build/gtest/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/au_crustcrawler_base/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/dynamixel_motor/dynamixel_driver/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/dynamixel_motor/dynamixel_motor/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/dynamixel_motor/dynamixel_tutorials/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/dynamixel_motor/dynamixel_controllers/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_arduino/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_client/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_msgs/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_python/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_xbee/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/dynamixel_motor/dynamixel_msgs/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/beginner_tutorials/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/quickui/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/single_motor/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/single_motor2/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/au_crustcrawler_moveit/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_server/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_embeddedlinux/cmake_install.cmake")
  INCLUDE("/home/ubuntu/catkin_ws/build/rosserial/rosserial_windows/cmake_install.cmake")

ENDIF(NOT CMAKE_INSTALL_LOCAL_ONLY)

IF(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
ELSE(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
ENDIF(CMAKE_INSTALL_COMPONENT)

FILE(WRITE "/home/ubuntu/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}" "")
FOREACH(file ${CMAKE_INSTALL_MANIFEST_FILES})
  FILE(APPEND "/home/ubuntu/catkin_ws/build/${CMAKE_INSTALL_MANIFEST}" "${file}\n")
ENDFOREACH(file)
