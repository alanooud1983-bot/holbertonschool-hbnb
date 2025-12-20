# High-Level Package Diagram

This diagram represents the high-level layered architecture of the HBnB application.
The Presentation layer communicates with the Business Logic layer through a Facade,
which coordinates interactions with the Persistence layer.

```mermaid
flowchart LR
    Presentation[Presentation Layer]
    Business[Business Logic Layer<br/>Facade]
    Persistence[Persistence Layer]

    Presentation --> Business
    Business --> Persistence
