; user-defined function

#|
The mass-decay function calculates the remaining mass 
of an atom after a period of decay.
|#

(defun massdecay (mass time halflife)
    (* mass (expt E (* (/ (- 0 log_2) halflife) time)))
	#|
	The formula used:
		m = m0 * E ^ (-lambda*t)
		lambda = -ln2 / halflife
	|#
)

; main function

#|
The main function applies the mass-decay function 
with user's inputs to calculate the remaining mass 
of an atom and compare that mass with half of the 
initial mass.
|#


(defconstant E 2.7)	; define constant E
(defconstant log_2 0.6931)
(defvar mass)
(defvar halflife)
(defvar time)
(defvar re)
(setq mass (read))
(setq halflife (read))
(setq time (read))
(setq re (massdecay mass time halflife))
(if (> re (/ mass 2))
(write  mass)
(write  re))
