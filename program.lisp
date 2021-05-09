; user-defined function

#|
The mass-decay function calculates the remaining mass 
of an atom after a period of decay.
|#

(defun mass-decay(mass time halflife)
    (defconstant E 2.7)	; define constant E
    (* mass (expt E (* (/ (-(log 2)) halflife) time)))
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

(defun main()
    (princ "Enter the initial mass: ")
    (setq mass (read))
    (terpri)
    (princ "Enter the half-life time: ")
    (setq half-life (read))
    (terpri)
    (princ "Enter the decay time: ")
    (setq time (read))
    (terpri)
    (setq re (mass-decay mass time half-life))
    (if (> re (/ mass 2))
    (format t "The remaining mass ~F is greater than half of the initial mass ~F" re mass)
    (format t "The remaining mass ~F is smaller than half of the initial mass ~F" re mass))
)

(main)