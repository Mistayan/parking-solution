from parking_solution import ParkingSolution

if __name__ == "__main__":
    accepts = {"moto": 1, "car": 1, "van": 3}  # vehicle_allowed: vehicle_size
    park = ParkingSolution(4, 6, accepts)  # Will generate a parking with 5 lines, 4 spots each
    # we assume that whoever parks takes the first valid slot encountered
    park + "tuctuc"
    park.allow_vehicles({"tuctuc": 1})
    park + "tuctuc"
    park + "car"
    for _ in range(7):
        park + "van"
    park + "moto"
    park - "van"
    park + "moto"
    park + "van"
    park + ["moto", "car"]
    park + None
    park.show()
    park.show()
    print(f"total park spaces: {park.get_total()}"
          f" used spots : {park.get_used()}"
          f" remaining : {park.get_remaining()}")
    print(f"cars : {park.count('car')}")
    print(f"vans : {park.count('van')}")
    print(f"motos : {park.count('moto')}")
    print(f"tuctucs : {park.count('tuctuc')}")
