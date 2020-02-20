function netcdftogeotiff = netcdf_to_tiff(args)
	filename = args.arg1;
	ncvar = args.arg2;
	timesno = args.arg3;
	outputdir = args.arg4;
	a = ncread(filename, ncvar);
	for avgiter = 1:timesno
	    A = single(rot90(a(:,:,avgiter)));
		A(A == -99999.0)= 0;
	    t = Tiff(strcat(outputdir, strcat(num2str(avgiter),'_GRACE_TWS_JPL_Mascons.tif')), 'w'); 
	    tagstruct.ImageLength = size(A, 1); 
	    tagstruct.ImageWidth = size(A, 2); 
	    tagstruct.Compression = Tiff.Compression.None; 
	    tagstruct.SampleFormat = Tiff.SampleFormat.IEEEFP; 
	    tagstruct.Photometric = Tiff.Photometric.MinIsBlack; 
	    tagstruct.BitsPerSample = 32; 
	    tagstruct.SamplesPerPixel = 1; 
	    tagstruct.PlanarConfiguration = Tiff.PlanarConfiguration.Chunky; 
	    t.setTag(tagstruct); 
	    t.write(A); 
	    t.close();
	    world = fopen(strcat(outputdir, strcat(num2str(avgiter),'_GRACE_TWS_JPL_Mascons.tfw')),'w');
		%Pretty basic, 6 rows:
		%First row is x-pixel resolution
		%Second and third rows are so-called "rotational components" but are set to zero in the case of an unrotated mapsheet.
		%The fourth row is the y-pixel resolution. The negative sign indicates that the image y-axis is positive down which is the opposite from real world coordinates.
		%The 5th and 6th rows are the Easting and Northing of the upper left pixel (0,0 in image coordinates).
	    fprintf(world, '0.5\r\n0.0\r\n0.0\r\n-0.5\r\n0.25\r\n89.75');
	    fclose(world);
	end