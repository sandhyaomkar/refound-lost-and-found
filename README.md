# \# RE:FOUND – Lost and Found Item Management Portal

# 

# A web-based Lost and Found Item Management Portal built using \*\*Python Flask, MySQL, HTML, CSS, JavaScript and Docker\*\*.

# 

# RE:FOUND aims to help users discover lost and found items through searchable listings and location-based filtering.

# 

# \## Features

# 

# \- Browse lost and found item listings.

# \- Search items using keywords.

# \- Filter items by city, category and item type.

# \- Filter listings by date.

# \- View item information through APIs.

# \- Store item details and recovery status in MySQL.

# \- Docker-based application setup.

# \- Automated testing using pytest and GitHub Actions.

# 

# \## Technologies Used

# 

# | Technology | Purpose |

# |---|---|

# | Python | Backend programming |

# | Flask | Web framework |

# | MySQL | Database |

# | HTML, CSS, JavaScript | Frontend |

# | Docker | Containerization |

# | Git and GitHub | Version control |

# | GitHub Actions | Continuous Integration |

# | Pytest | Automated testing |

# 

# \## Database Structure

# 

# The application uses three main tables:

# 

# \- \*\*cities\*\* – stores city names and geographical coordinates.

# \- \*\*categories\*\* – stores item categories.

# \- \*\*items\*\* – stores lost/found item details, descriptions, locations, photos and recovery status.

# 

# \## Project Structure

# 

# ```text

# refound/

# ├── .github/

# │   └── workflows/

# │       └── ci.yml

# ├── static/

# ├── templates/

# ├── tests/

# ├── .env.example

# ├── .gitignore

# ├── app.py

# ├── db.py

# ├── Dockerfile

# ├── docker-compose.yml

# ├── requirements.txt

# ├── schema.sql

# ├── seed.py

# └── README.md

# ```

# 

# \## Run Locally Using Docker

# 

# 1\. Install Docker Desktop.

# 2\. Clone the repository:

# 

# ```bash

# git clone https://github.com/sandhyaomkar/refound-lost-and-found.git

# ```

# 

# 3\. Navigate into the project:

# 

# ```bash

# cd refound-lost-and-found

# ```

# 

# 4\. Configure environment variables using `.env.example` as a reference.

# 5\. Start the application:

# 

# ```bash

# docker compose up --build

# ```

# 

# 6\. Open the application:

# 

# http://localhost:5000

# 

# \## Run Tests

# 

# Install pytest and run:

# 

# ```bash

# pip install -r requirements.txt

# pip install pytest

# python -m pytest

# ```

# 

# \## Continuous Integration

# 

# GitHub Actions automatically runs the test suite when code is pushed to the main branch or a pull request is created.

# 

# \## Future Enhancements

# 

# \- User registration and login.

# \- Report lost or found items.

# \- Smart matching of lost and found items.

# \- Map-based item discovery.

# \- Item claim and recovery workflow.

# 

# \## Author

# 

# \*\*Sandhya Omkar\*\*

# 

# GitHub: https://github.com/sandhyaomkar

# 

# \---

# 

# \*RE:FOUND – Helping lost belongings find their way home.\*

