import tensorflow as tf
from tensorflow.keras import layers, models

# Define the VAE model
def build_vae(input_shape, latent_dim):
    # Encoder
    encoder_inputs = layers.Input(shape=input_shape)
    x = layers.Flatten()(encoder_inputs)
    x = layers.Dense(256, activation='relu')(x)
    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)

    # Reparameterization trick
    def sampling(args):
        z_mean, z_log_var = args
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

    z = layers.Lambda(sampling, output_shape=(latent_dim,))([z_mean, z_log_var])

    # Decoder
    decoder_inputs = layers.Input(shape=(latent_dim,))
    x = layers.Dense(256, activation='relu')(decoder_inputs)
    x = layers.Dense(np.prod(input_shape), activation='sigmoid')(x)
    decoder_outputs = layers.Reshape(input_shape)(x)

    encoder = models.Model(encoder_inputs, [z_mean, z_log_var, z], name='encoder')
    decoder = models.Model(decoder_inputs, decoder_outputs, name='decoder')

    vae_outputs = decoder(encoder(encoder_inputs)[2])
    vae = models.Model(encoder_inputs, vae_outputs, name='vae')

    return vae, encoder, decoder

# Build and compile the VAE model
input_shape = (187,)  # Adjust the input size based on your nsamples
latent_dim = 100  # You may need to adjust the latent dimension based on your data
vae, encoder, decoder = build_vae(input_shape, latent_dim)
vae.compile(optimizer='adam', loss='binary_crossentropy')

# Training loop (you need to replace this with your actual data)
vae.fit(x_train, x_train, epochs=num_epochs, batch_size=batch_size)
