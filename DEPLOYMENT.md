# Bariatric Insurance Navigator — Demo Deployment

## Important
This build is a prototype demonstration. Do not enter PHI, real member IDs, or other patient-identifying information
unless and until Banner approves the hosting environment, security controls, authentication, storage, and workflow.

## Option 1: Streamlit Community Cloud — demo only
This is the simplest way to give reviewers a web link for a non-PHI prototype.

1. Create a GitHub repository containing the files in this folder.
2. Push `app.py`, `requirements.txt`, `.streamlit/config.toml`, and the rest of the project.
3. In Streamlit Community Cloud, create a new app from that GitHub repository.
4. Set the entry file to `app.py`.
5. Deploy and share the generated URL with reviewers.
6. Keep the prototype warning visible and use fictional/test data only.

Do not use this route for real patient data unless Banner explicitly approves it.

## Option 2: Banner-approved Azure / container hosting
A `Dockerfile` is included so IT can containerize the application.

Local Docker test:
    docker build -t bariatric-insurance-navigator .
    docker run -p 8501:8501 bariatric-insurance-navigator

Then open:
    http://localhost:8501

Banner IT can use the same container as a starting point in an approved Azure or internal environment and add:
- Banner/Microsoft Entra ID authentication
- role-based access
- HTTPS / managed certificates
- approved data storage
- audit logging
- session timeout
- monitoring
- backup/retention rules
- EHR integration if approved

## Recommended review path
1. Demo the non-PHI version first.
2. Obtain workflow/leadership approval.
3. Obtain IT/security/compliance review.
4. Decide the approved production hosting environment.
5. Add authentication and production data controls.
6. Pilot with a small staff group before broad use.
