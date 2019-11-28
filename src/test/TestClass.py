import sys, getopt


if __name__ == '__main__':
    input_raster_data = r'#'
    output_table = r'#'
    feature_zone = r'#'

    myopts, args = getopt.getopt(sys.argv[1:], "i:o:f:")
    for o, a in myopts:
        if o == '-i':
            input_raster_data = a
        elif o == '-o':
            output_table = a
        elif o == '-f':
            feature_zone = a
        else:
            print(
            "Usage: %s -i input_raster_data_directory -o output_table_directory -f feature_zone" %
            sys.argv[0])
    print 'before printing parameters'
    print input_raster_data
    print output_table
    print feature_zone
    print 'after printing parameters'