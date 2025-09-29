using Microsoft.EntityFrameworkCore;
using Welldoc.Api.Data.Entities;

namespace Welldoc.Api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    public DbSet<Patient> Patients => Set<Patient>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Patient>(b =>
        {
            b.HasKey(p => p.PatientID);
            b.Property(p => p.PatientID).ValueGeneratedOnAdd();
            b.Property(p => p.PatientFirstName).HasMaxLength(200).IsRequired();
            b.Property(p => p.PatientLastName).HasMaxLength(200).IsRequired();
            b.Property(p => p.RegistrationDatetime).IsRequired();
        });
    }
}
