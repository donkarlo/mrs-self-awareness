# Install script for directory: /home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/src/sauavs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sauavs/srv" TYPE FILE FILES
    "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/src/sauavs/srv/AddTwoInts.srv"
    "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/src/sauavs/srv/Vec4.srv"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sauavs/cmake" TYPE FILE FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/build/sauavs/catkin_generated/installspace/sauavs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/include/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/share/roseus/ros/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/share/common-lisp/ros/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/share/gennodejs/ros/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/lib/python3/dist-packages/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/devel/lib/python3/dist-packages/sauavs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/build/sauavs/catkin_generated/installspace/sauavs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sauavs/cmake" TYPE FILE FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/build/sauavs/catkin_generated/installspace/sauavs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sauavs/cmake" TYPE FILE FILES
    "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/build/sauavs/catkin_generated/installspace/sauavsConfig.cmake"
    "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/build/sauavs/catkin_generated/installspace/sauavsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sauavs" TYPE FILE FILES "/home/donkarlo/Dropbox/projs/research/artificial-intelligence/self-awareness/selfaware-drones/rosws/src/sauavs/package.xml")
endif()

