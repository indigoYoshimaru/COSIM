#|
The main function applies the mass-decay function 
with user's inputs to calculate the remaining mass 
of an atom and compare that mass with half of the 
initial mass.
|#

(defun sum (x sumterm)
    (+ x sumterm)   
)

(defun subtract (x minusterm)
    (* (- x minusterm) minusterm)
)

(defconstant A 2.9)
(defconstant B 6)
(defvar res)
(defvar x)
(setq x 1)

(if (< A B) 
    (setq res (sum x A))
    (setq res (subtract x B)))

(write res)