# GANGogh

[Blog post](https://towardsdatascience.com/gangogh-creating-art-with-gans-8d087d8f74a1)

## Requirements

- OS: Windows or Linux

- Python 3.5.6

  [pyenv](https://github.com/pyenv/pyenv) is recommended

- Python dependencies

  ```sh
  pip install -r requirements.txt
  ```

- Tensorflow with [GPU support](https://www.tensorflow.org/install/gpu) for v1.2.1 (macOS not supported)

  Tensorflow v1.2.1 [requires](https://www.tensorflow.org/install/source#tested_build_configurations) CUDA 8 and cuDNN 5.1

  To test if Tensorflow GPU is correctly set up [run](https://www.tensorflow.org/api_docs/python/tf/test/is_gpu_available):

  ```python
  import tensorflow as tf
  tf.test.is_gpu_available()
  ```

## Usage

### 1. Gather training data

We used training data from wikiart.org, but any training data will do.

You can download the training data from:

- [this torrent](http://academictorrents.com/details/1d154cde2fab9ec8039becd03d9bb877614d351b) or
- [Google Drive file](https://drive.google.com/file/d/1yHqS2zXgCiI9LO4gN-X5W18QYXC5bbQS/view?usp=sharing)

If both of those fail, consider using [scrape_wiki.py](misc/scrape_wiki.py) as a last resort.

### 2. Prepare the training data

Adjust the variables `ORIGINAL_IMAGES_PATH` and `RESIZED_IMAGES_PATH` in [settings.py](settings.py) accordingly.

Use [resize_rename.py](misc/resize_rename_images.py) to create image data set of 64x64 pieces of art scraped from [wikiart.org](https://www.wikiart.org):

```python
python misc/resize_rename_images.py
```

### 3. Modify files

Update the `styles` variable in [wikiart_genre.py](tflib/wikiart_genre.py) dictating the number of training images per genre. If using the traning data set linked, above, use the following:

```python
styles = {
  'abstract': 14999,
  'animal-painting': 1798,
  'cityscape': 6598,
  'figurative': 4500,
  'flower-painting': 1800,
  'genre-painting': 14997,
  'landscape': 15000,
  'marina': 1800,
  'mythological-painting': 2099,
  'nude-painting-nu': 3000,
  'portrait': 14999,
  'religious-painting': 8400,
  'still-life': 2996,
  'symbolic-painting': 2999
}
```

<!-- markdownlint-disable no-trailing-punctuation -->

### 4. Make art!

<!-- markdownlint-enable no-trailing-punctuation -->

Run [gangogh.py](gangogh.py)

```python
python gangogh.py
```

## Credits

Code heavily inspired and built off of the improved wasserstein GAN training code available and found at [igul222/improved_wgan_training](https://github.com/igul222/improved_wgan_training)
