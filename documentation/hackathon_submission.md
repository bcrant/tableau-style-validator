## Inspiration
In my new role, I am working on customer facing dashboards, and part of my responsibility is to enforce the style standards where the dashboards are embedded onto the dashboards. 

As someone who sees colors slightly differently than others, I decided it was best to outsource this responsibility to a computer. In addition to colors, Tableau dashboards can include many hidden components that are easy to overlook or miss during code review / quality assurance.

## What it does
The Tableau Style Validator tests a Workbook for compliance with a given set of design style standards. 
Company colors, specific fonts, font sizes are the primary scope here. I’m colorblind and thought it would be nice to QA my dashboards programmatically.

## How we built it
See [Tableau Style Validator Architecture](https://briancrant.com/wp-content/uploads/2021/06/TableauStyleValidatorArchitecture.pdf) for a breakdown of the projects inner-workings. 

## Challenges we ran into
I was slowed down for about a week troubleshooting my local environment on new work laptop with Mac M1 chip.
I'll spare you _all_ the details since it is not of much interest to this project, but sparknotes version is...
- the Mac M1 chip is not fully supported on Python 3.8 
- the current AWS Lambda Python runtime is Python 3.8
- not all the Python libraries used in this project are compatible with Python 3.8 on the Mac M1 chip

I ended up having install Docker using Rosetta, a terminal able to translate distributions built for x86-64 processor to arm64 (Mac M1), use that version of Docker to build the Python 3.8 dependencies for AWS Lambda, but some Python packages in this project are not compatible with Python 3.8 on Mac M1, so I ended having to build a separate environment on Python 3.9 locally.

## Accomplishments that we're proud of
- Helping out my fellow 8% of humans that are colorblind.
- Getting the project this far (releasable) in just a few weeks.
- This is my first project to include multiple options for deployment 
    - Run locally as a script
    - Run via command line interface 
    - Deploy via serverless cloud implementation

## What we learned
Time permitting, I would love to have taken what I have learned about the structure of Tableau XML documents and expand the Tableau Document API to permit updates to workbooks based on the Style Validator.

## What's next for Tableau Style Validator
- Add formatted Slack output for all style elements
  - Slack output is missing some of CLI features: Padding, Margins, Borders       
- Add support for Mark colors
- Add support for Table style elements
  - Logic complete, just need outputs
- Add flags to enable / disable testing against certain elements (padding, margins, etc) or test only font styles for instance. 