; user-defined function
(defun wavelength (f)
        (/ c f)
)

#| main function
using user-defined function
to classify light-power:
0 is low
|#

(defconstant c 3)
(defvar f)
(defvar w)
(defvar p)
(setq f (read))
(setq w (wavelength f))
(if(< w (/ 1 2))
(setq p 0))