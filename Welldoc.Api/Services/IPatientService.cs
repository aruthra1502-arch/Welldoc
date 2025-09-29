namespace Welldoc.Api.Services;

public interface IPatientService
{
    Task<long> CreatePatientAsync(string firstName, string lastName);
}
