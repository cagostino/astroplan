# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from astroplan import Observer, get_moon
from astropy.time import Time
from astropy.coordinates import EarthLocation, get_sun
import astropy.units as u
from numpy.testing import assert_allclose

def test_illumination():
    time = Time(['1990-01-01 00:00:00', '1990-03-01 06:00:00',
                 '1990-06-01 12:00:00', '1990-11-01 18:00:00'])
    location = EarthLocation.from_geodetic(-155*u.deg, 19*u.deg, 0*u.m)
    obs = Observer(location)
    # Get illumination via time
    illumination1 = obs.moon_illumination(time)

    moon = get_moon(time, obs.location, obs.pressure)
    sun = get_sun(time)
    # Get illumination via sun and moon
    illumination2 = obs.moon_illumination(moon=moon, sun=sun)
    assert all(illumination1 == illumination2)

    # Get illumination using jplephem instead of PyEphem
    moon_jplephem = get_moon(time, obs.location, obs.pressure,
                             use_pyephem=False)
    illumination3 = obs.moon_illumination(moon=moon, sun=sun)
    assert_allclose(illumination1, illumination3, atol=1)

    # Run print_pyephem_illumination() for PyEphem's solution
    pyephem_illumination = [0.15475513880925418, 0.19484233284757257,
                            0.6170840254669668, 0.9780219372563843]

    assert_allclose(illumination1, pyephem_illumination, atol=1)


def print_pyephem_illumination():
    """
    To run, use:
    python -c "from astroplan.tests.test_moon import print_pyephem_illumination as f; f()"
    """
    time = Time(['1990-01-01 00:00:00', '1990-03-01 06:00:00',
                 '1990-06-01 12:00:00', '1990-11-01 18:00:00'])
    location = EarthLocation.from_geodetic(-155*u.deg, 19*u.deg, 0*u.m)

    import ephem
    moon = ephem.Moon()
    pe_obs = ephem.Observer()
    pe_obs.lat = location.latitude.to(u.degree).to_string(sep=':')
    pe_obs.lon = location.longitude.to(u.degree).to_string(sep=':')
    pe_obs.elevation = location.height.to(u.m).value
    illuminations = []
    for t in time:
        pe_obs.date = t.datetime
        moon.compute(pe_obs)
        illuminations.append(moon.moon_phase)
    print(illuminations)
