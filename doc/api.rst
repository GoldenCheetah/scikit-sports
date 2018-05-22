######################
``scikit-sports`` API
######################

This is the full API documentation of ``scikit-sports``

.. _data_management_ref:

Data-management
===============

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/

   Rider

.. _extraction_ref:

Extraction
==========

.. automodule:: sksports.extraction
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/
   :template: function.rst

   extraction.activity_power_profile
   extraction.acceleration
   extraction.gradient_activity
   extraction.gradient_elevation
   extraction.gradient_heart_rate

.. _metrics_ref:

Metrics
=======

.. automodule:: sksports.metrics
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/
   :template: function.rst

   metrics.normalized_power_score
   metrics.intensity_factor_score
   metrics.training_stress_score
   metrics.training_load_score
   metrics.mpa2ftp
   metrics.ftp2mpa
   metrics.aerobic_meta_model

Single cycling activity
-----------------------

.. autosummary::
   :toctree: generated/
   :template: function.rst

   metrics.normalized_power_score
   metrics.intensity_factor_score
   metrics.training_stress_score
   metrics.training_load_score
   
Power-profile
-------------

.. autosummary::
   :toctree: generated/
   :template: function.rst

   metrics.aerobic_meta_model

.. _models_ref:

Models
======

.. automodule:: sksports.model
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports
       
Power
-----

.. autosummary::
   :toctree: generated/
   :template: function.rst

   model.strava_power_model

.. _utils_ref:

Utilities
=========

.. automodule:: sksports.utils
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/
   :template: function.rst

   utils.validate_filenames

.. _io_ref:

IO interaction
==============

.. automodule:: sksports.io
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/
   :template: function.rst

   io.bikeread

.. _datasets_ref:

Datasets
========

.. automodule:: sksports.datasets
    :no-members:
    :no-inherited-members:

.. currentmodule:: sksports

.. autosummary::
   :toctree: generated/
   :template: function.rst

   datasets.load_fit
   datasets.load_rider
