using Welldoc.Api.Data;
using Welldoc.Api.Data.Entities;

namespace Welldoc.Api.Services;

public class PatientService : IPatientService
{
    private readonly AppDbContext _db;
    public PatientService(AppDbContext db) => _db = db;

    public async Task<long> CreatePatientAsync(string firstName, string lastName)
    {
        var entity = new Patient
        {
            PatientFirstName = firstName.Trim(),
            PatientLastName  = lastName.Trim(),
            RegistrationDatetime = DateTime.UtcNow
        };
        _db.Patients.Add(entity);
        await _db.SaveChangesAsync();
        return entity.PatientID;
    }
}
