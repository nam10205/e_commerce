# Visual Paradigm Open Java API sources

The final project is `../assignment06_multimodal_search_final.vpp`.
Opening it does not require installing a custom plugin.

`ApiBuilder.java` and `plugin.xml` create the original three UML diagrams.
`ApiReference.java` and `reference_plugin.xml` provide the final use case
layout and cyan fill. Run the reference plugin after the initial builder.
It preserves the Component and Sequence models, creates 12 use cases,
6 includes, 2 extends, 3 generalizations, and 2 actor associations, and
saves the project through Visual Paradigm.

The reference plugin takes the submission directory as its first argument.
Its optional second argument `verify` reopens/checks the project without
modifying it and exports the three reference PNGs. The verification results
are written to `demo/uml_verification.json`.

These Java files are source evidence for the modeling process. They need
the Visual Paradigm plugin API to compile and Visual Paradigm to execute.
There are no license files or application configuration files in the package.
