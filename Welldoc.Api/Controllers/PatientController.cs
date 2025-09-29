using Microsoft.AspNetCore.Mvc;
using Welldoc.Api.Services;

namespace Welldoc.Api.Controllers;

[ApiController]
[Route("api/patient")]
public class PatientController : ControllerBase
{
    private readonly IPatientService _patientService;
    public PatientController(IPatientService patientService) => _patientService = patientService;

    // POST /api/patient/create
    [HttpPost("create")]
    public async Task<IActionResult> Create([FromBody] CreatePatientRequest request)
    {
        if (request is null || string.IsNullOrWhiteSpace(request.PatientFirstName) || string.IsNullOrWhiteSpace(request.PatientLastName))
            return BadRequest("PatientFirstName and PatientLastName are required.");

        var id = await _patientService.CreatePatientAsync(request.PatientFirstName, request.PatientLastName);
        return Ok(new CreatePatientResponse { PatientID = id });
    }
}

public class CreatePatientRequest
{
    public string? PatientFirstName { get; set; }
    public string? PatientLastName  { get; set; }
}
public class CreatePatientResponse
{
    public long PatientID { get; set; }
}
