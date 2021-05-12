; user-defined function, test the simple one first

#|
The mass-decay function calculates the remaining mass 
of an atom after a period of decay.
|#

(defun massdecay (mass time halflife)
    ; (* (/ (- mass halflife) halflife) time)
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
; no requirement on implement the log function

(defconstant log_2 0.6931)
(defconstant E 2.7)	; define constant E
(setq re (massdecay 1 2 3))



