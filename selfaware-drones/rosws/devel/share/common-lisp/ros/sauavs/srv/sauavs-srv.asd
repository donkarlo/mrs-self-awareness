
(cl:in-package :asdf)

(defsystem "sauavs-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "AddTwoInts" :depends-on ("_package_AddTwoInts"))
    (:file "_package_AddTwoInts" :depends-on ("_package"))
    (:file "Vec4" :depends-on ("_package_Vec4"))
    (:file "_package_Vec4" :depends-on ("_package"))
  ))