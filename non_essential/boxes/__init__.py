"""
max dimensions (width & height) of the material
    if the part is larger than the max dimensions then part must be `pieced` together

kerf

    if our laser beam has a width of 20 mm (kerf - aka the thickness of the blade)
    and we do not factor this into our calculations (i.e., a kerf value of 0)
    then we would take off 10 mm too much material from the edge of the shape
    if we use a kerf value of 10, then 5 mm too much material from the edge would be taken off
    if we use a kerf value of 20 then 0 mm too much material would be taken off

   -10 (-5) --> 15 (even looser fit -- taking off 15 mm too much)
     0  (0) --> 10 (looser fit)
     8  (4) -->  6
    10  (5) -->  5
    12  (6) -->  4
    14  (7) -->  3
    16  (8) -->  2
    20 (10) -->  0 (tighter fit)
    30 (15) -->  +5 (even tighter fit -- adding on additional material)

    The burn correction value is the half (i.e., radius) of the laser's diameter (i.e., width or kerf)

    Note: The way the burn param works is a bit counter intuitive. Bigger burn values make a
    tighter fit. Smaller values make a looser fit.

    Small changes in the burn param can make a notable difference. Typical steps for adjustment
    are 0.01 mm or even 0.005 mm to choose between different amounts of force needed to press
    plywood together.

fingers

    with of fingers / space-between-fingers is a multiple (whole or fractional) of the material thickness
    with of the beginning / end space is a multiple (whole or fractional?) of the finger width
    the number of fingers plus space-between-fingers is always an odd number


"""
