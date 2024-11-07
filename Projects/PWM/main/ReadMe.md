To speed up the microcontroller, follow these steps:

1. Run `idf.py menuconfig`.
2. Navigate to **Component config -> ESP System Settings -> CPU Frequency**.
3. Choose **240 MHz**. You can select the option using the space bar.
4. Press **S** to save, then press **Enter** twice, and finally press **Q** to quit.

You can make a fancier delivery using Serial Studio.

To enable Serial Studio output

1. Run `idf.py menuconfig`
2. Navigate to **Example Configuration-> Enable log that can be parsed by Serial Studio**.

This is the serial studio program. 

https://github.com/Serial-Studio/Serial-Studio