import concurrent.futures
from functools import partial
from pathlib import Path
import multiprocessing
import upscale

def process_image(img_path, model, output_dir, skip_existing):
    img_path = Path(img_path)
    output_dir = Path(output_dir)
    upscale_module = upscale.Upscale(model, img_path, output_dir, skip_existing)  # initialize a new Upscale object
    upscale_module.run()  # process the image

def main():
    input_dir = input("Enter the path to the input directory: ")
    output_dir = input("Enter the path to the output directory: ")
    model = input("Enter the path to the model file: ")
    skip_existing = True if input("Skip existing files? (y/n): ") == "y" else False
    verbose = True if input("Verbose? (y/n): ") == "y" else False

    input_folder = Path(input_dir)
    images = list(input_folder.glob('*'))  # list of image file paths

    # Create a new function with some arguments pre-filled
    func = partial(process_image, model=model, output_dir=output_dir, skip_existing=skip_existing)

    num_cpus = multiprocessing.cpu_count()
    with concurrent.futures.ProcessPoolExecutor(max_workers=-1) as executor:
        list(executor.map(func, images))  # Consume the generator to start the computations

if __name__ == "__main__":
    main()
