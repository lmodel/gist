<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>

# gist

GIST (Semantic Arts, Upper Enterprise Ontology) - LinkML Schema

> **Two ways in.** This README is one; the other is a docent. Install
> [`ktl-docent`](https://github.com/noelmcloughlin/knowledge-trust-ladder) into
> whatever agent you already use -
> `npx skills add noelmcloughlin/knowledge-trust-ladder --skill ktl-docent --yes` -
> and ask it anything about this project. It answers from `.lokf/knowledge/`,
> the checked part of what the project knows, says how far each answer has been
> trusted (still a draft, checked by automation only, or confirmed by a named
> person), opens the source for exact values, and records what it couldn't
> answer so the gap gets filled. One door for a person at a prompt, an agent
> reading this file, or a chatbot that can load a skill. **Agents:** if
> `.lokf/knowledge/index.md` exists, read it first - `llms.txt` says how to
> weigh it.

## Documentation Website

[https://lmodel.github.io/gist](https://lmodel.github.io/gist)

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files (edit these)
  * [gist](src/gist)
    * [schema/](src/gist/schema) -- LinkML schema
      (edit this)
    * [datamodel/](src/gist/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/).
To list all pre-defined commands, run `just` or `just --list`.

## License and attribution

gist is Semantic Arts' upper ontology, published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This schema is
derived from the gist 14.1.0 release: the OWL modules are converted to LinkML
by [scripts/gist_to_linkml.py](scripts/gist_to_linkml.py), their RDFS
annotations and subclass assertions are folded into the schema, and SSSOM
mappings to other vocabularies are added from [src/gist/mappings/](src/gist/mappings).
The release is kept unmodified in [upstream/](upstream/gist14.1.0_webDownload)
with its [LICENSE.txt](upstream/gist14.1.0_webDownload/LICENSE.txt). The code
in this repository is Apache-2.0 ([LICENSE](LICENSE)).

Semantic Arts also asks that terms used from gist stay in the gist namespace
and that nobody else defines terms there. The schema and every generated
artefact hold to both:

* **`gist:`** (`https://w3id.org/semanticarts/ns/ontology/gist/`) and
  **`gistd:`** are Semantic Arts' namespaces. Every gist class, property and
  individual keeps its gist IRI.
* **`gist_linkml:`** (`https://w3id.org/lmodel/gist/`) is this project's
  namespace. It holds only what the LinkML rendering adds: the schema
  documents, the `GistThing` mixin, the enums, the subsets, the SHACL shapes,
  and the LinkML element definitions the OWL links to the gist terms they
  render.
* Tests in [tests/test_schema_validation.py](tests/test_schema_validation.py)
  and [tests/test_generated_artifacts.py](tests/test_generated_artifacts.py)
  check both rules against the vendored release.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
