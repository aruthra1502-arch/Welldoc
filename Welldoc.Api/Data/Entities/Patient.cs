namespace Welldoc.Api.Data.Entities;

public class Patient
{
    public long PatientID { get; set; }
    public string PatientFirstName { get; set; } = default!;
    public string PatientLastName { get; set; } = default!;
    public DateTime RegistrationDatetime { get; set; }
}
