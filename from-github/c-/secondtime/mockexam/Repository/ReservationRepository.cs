using mockexam.Data;
using System;
using System.IO;
using mockexam.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

namespace mockexam.Repositories
{  
    //ef core database context used to intect with the reservations table
    public class ReservationRepository : IReservationRepository
    {
        private readonly AppDbContext _context;
        // File path for storing reservations in CSV format
        private readonly string _filePath = "Data/reservations.csv";

        // Header for the CSV file

        private const string Header = "ReservationId,Brand,Model,Processor,RAM,Storage,ScreenSize,Price,ReservationDate";

       // Constructor that initializes the repository with the database context receives an instace of appdbcontetc cia dependcy injecton
        public ReservationRepository(AppDbContext context)
        {
            _context = context; //store the databse conetx for later use in crd methofds
        }


        private void EnsureFile()

        {  // get the directory of the file path
            var dir = Path.GetDirectoryName(_filePath);
            // Check if the directory exists, if not, create it
            if (!Directory.Exists(dir))
            {
                // If the directory is null, create the directory
                if (dir != null)
                {
                    Directory.CreateDirectory(dir);
                }
            } // Check if the file exists, if not, create it with the header
            if (!File.Exists(_filePath))
            {
                File.WriteAllText(_filePath, Header + Environment.NewLine);
            }
        }

        // Retrieves all reservations from the CSV file

        public IEnumerable<Reservation> GetAll()
        {
            EnsureFile();
            // Read all lines from the CSV file, skipping the header line

            var lines = File.ReadAllLines(_filePath).Skip(1);
            var reservations = new List<Reservation>();

            foreach (var line in lines)
            {
                var parts = line.Split(',');
                if (parts.Length == 9)
                // Check if the line has the correct number of parts (9)
                {
                    var reservation = new Reservation
                    { // Create a new Reservation object and populate its properties
                        ReservationId = int.Parse(parts[0]),
                        Brand = parts[1],
                        Model = parts[2],
                        CustomerAdress = parts[3],
                        CustomerName = parts[4],
                        CustomerEmail = parts[5],
                        CustomerPhone = parts[6],
                        QuantityLaptop = decimal.Parse(parts[7]),
                        TotalPrice = decimal.Parse(parts[8])




                    };

                }
            }
            return reservations;
        }
        // Retrieves a reservation by its ID from the CSV file

        // /// <summary>

        /// Gets a reservation by its ID.
        public Reservation GetReservationById(int id) =>
           GetAll().FirstOrDefault(r => r.ReservationId == id)!;
           // Get all existing reservations into a list
           //Returns the first element that matches a condition (if given).
        //If no match is found, it returns the default value for that type.

        public void AddReservation(Reservation reservation)
        // Adds a new reservation to the CSV file
        {
            var reservations = GetAll().ToList();
            // Ensure the reservation ID is unique by assigning a new ID
            reservation.ReservationId = reservations.Any() ? reservations.Max(r => r.ReservationId) + 1 : 1;
             // Assign a new ID:
            // If there are existing reservations → new ID = max existing ID + 1
             // Otherwise → new ID = 1
            
            reservations.Add(reservation);
            WriteToFile(reservations); // Save updated list back to the file



        }

        public void UpdateReservation(Reservation reservation)
        {  // Get all reservations
            var reservations = GetAll().ToList();
            // Find the index of the reservation that matches the ID
            // If found, update the reservation at that index
            var idx = reservations.FindIndex(r => r.ReservationId == reservation.ReservationId);
            if (idx != -1)
            {
                reservations[idx] = reservation; // Replace it with the updated reservation
                // Write the updated list of reservations back to the file
                WriteToFile(reservations);
            }
        }

        public void DeleteReservation(int id)
        // Deletes a reservation by its ID from the CSV file
        {
            var reservations = GetAll()
                .Where(r => r.ReservationId != id) // Keep only reservations whose ReservationId is not equal to the id we want to remove.
                // Filter out the reservation with the specified ID
                .ToList();
            // Write the remaining reservations back to the file
            WriteToFile(reservations);

        }

        private void WriteToFile(IEnumerable<Reservation> reservations)
        {
            EnsureFile();
            // Ensure the file exists before writing

            var lines = new List<string> { Header };
            // Initialize the lines list with the header
            lines.AddRange(reservations.Select(r =>
                $"{r.ReservationId},{r.Brand},{r.Model},{r.CustomerAdress},{r.CustomerName},{r.CustomerEmail},{r.CustomerPhone},{r.QuantityLaptop},{r.TotalPrice}"));
            // Add each reservation as a formatted string to the lines list
            File.WriteAllLines(_filePath, lines);
        }










    }
}