# High-Level Package Diagram – HBnB

This diagram illustrates the high-level layered architecture of the HBnB application,
showing how the Presentation, Business Logic, and Persistence layers interact using
the Facade Pattern.

## Architecture Overview

```mermaid
classDiagram
direction LR

namespace Presentation_Layer {
  class API {
    +routes
    +request/response
  }

  class Controllers {
    +handle_requests()
  }
}

namespace Business_Logic_Layer {
  class Facade {
    +create_user()
    +create_place()
    +list_places()
    +create_review()
  }

  class Services {
    +validation()
    +business_rules()
  }

  class Models {
    +User
    +Place
    +Review
    +Amenity
  }
}

namespace Persistence_Layer {
  class Repositories {
    +save()
    +get_by_id()
    +list()
    +delete()
  }

  class Database {
    +connection
    +tables
  }
}

Presentation_Layer.API --> Presentation_Layer.Controllers
Presentation_Layer.Controllers --> Business_Logic_Layer.Facade : calls
Business_Logic_Layer.Facade --> Business_Logic_Layer.Services : orchestrates
Business_Logic_Layer.Services --> Business_Logic_Layer.Models : uses
Business_Logic_Layer.Facade --> Persistence_Layer.Repositories : data access
Persistence_Layer.Repositories --> Persistence_Layer.Database : CRUD
