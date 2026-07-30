using mockexam.Models;
namespace mockexam.Repositories
{
    public interface ILaptopRepository
    {
        List<Laptop> GetAllLaptops();

        Laptop GetLaptopById(int id);
    }
}