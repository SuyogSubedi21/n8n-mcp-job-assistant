from mcp.server.fastmcp import FastMCP

import db
import cv_fit

mcp = FastMCP("job-mcp", host="0.0.0.0", port=8000)


@mcp.tool()
def add_application(company: str, role: str, status: str = "applied") -> dict:
    """Save a new job application. status can be applied, interview, rejected or offer."""
    app_id = db.add_application(company, role, status)
    return {"id": app_id, "company": company, "role": role, "status": status}


@mcp.tool()
def update_status(company: str, status: str) -> dict:
    """Update an application's status. Status must be one of:
    applied, confirmation, interview, rejected, offer."""
    updated = db.update_status(company, status)
    if updated == 0:
        return {"ok": False, "message": f"No application found for {company}"}
    return {"ok": True, "company": company, "status": status}


@mcp.tool()
def get_stats() -> dict:
    """Get a count of applications by status."""
    return db.get_stats()


@mcp.tool()
def check_cv_fit(cv_text: str, required_skills: list[str]) -> dict:
    """Check how well a CV matches a job. Pass the full CV text and the list
    of skills required by the job description. Returns a score, matched
    and missing skills."""
    return cv_fit.check_fit(cv_text, required_skills)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")