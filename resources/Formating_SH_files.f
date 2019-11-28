              program main
c..... this program reads the GRACE SH files after remvoing tem mean formate it ..
       implicit double precision (a-h,o-z)
       parameter (nord=200, ntrm=nord*(nord+1)/2, nord2=2*nord)
       parameter (lmost=60)
       parameter (maxmon=160)
       DOUBLE PRECISION FACNM(0:nord2), CONV
       DOUBLE PRECISION CBAR, SBAR, D1, D2
       CHARACTER*10 TITLE(2), NAMEE
       CHARACTER*40 FORM, FORM2
       CHARACTER*128 TEMP
       COMMON/info/ TITLE,FORM,FORM2
       COMMON / POTNAM / IGEO
       COMMON / LEGEND / pn(0:nord),pnm(ntrm),rho(nord),iasect(nord),
     &                   slam(0:nord),clam(0:nord)
       COMMON / POTCOF / CNZ(NORD), CNM(NTRM), SNM(NTRM), GM, GMSCLE,
     &                  RE, MAXJ, MAXM, nfLD(NORD), MM1, MM2, MAXN
       COMMON / NORMC /  an(nord),bn(nord),anm(ntrm),
     &                   bnm(ntrm),fn0(0:nord),fnm(ntrm),enp1(ntrm),
     &                   enp2(ntrm),men(ntrm),mem(ntrm)
      dimension
     4  plmart(0:lmost,0:lmost),pdum(0:lmost)
     9  ,im(maxmon),error(0:lmost)
     2  ,clmave(0:lmost,0:lmost),slmave(0:lmost,0:lmost)
     2 ,rmat(3,3),indx(3),rhsc(3),rhss(3)
      character*15 mame
      character*22 mame1
      character*15 name
      character*18 name1
      character*3 imonth(maxmon)
      character*1 number(0:9)
      data number /'0','1','2','3','4','5','6','7','8','9'/

      mame='filtered_month_'
      name='filtered.month.'
      open (85,file='months_to_format.txt',status='unknown')
      read (85,*) nmonths
      print *, nmonths
       do 11 i=1,nmonths
      read (85,*) im(i)
      i0=im(i)/100
      i1=(im(i)-i0*100)/10
      i2=im(i)-i0*100-i1*10
      imonth(i)=number(i0)//number(i1)//number(i2)
11    continue
       do 200 i=1,nmonths


      mame1=mame//imonth(i)//'.txt'
      name1=name//imonth(i)

      open (12,file=mame1)
      open (20,file=name1)
      
  20   continue

 1101  FORMAT(A6,2I5,2F11.4,2F11.4,F4.0)
 1102  FORMAT(A128)
 201   format(a3,5x,i3,2x,i3,e19.12,e9.7)
 202   format(i3,i3,e9.7,1x,e9.7)
 983   format(a3,5x,i3)
 984   format(8x,i3)
 985   format(8x,i3,2x,i3,1x,e18.11,1x,e18.11)

 500    DO WHILE ( .TRUE. )
       READ(12,*,end=200) N, M, CBAR, SBAR
       write(20,985) N, M, CBAR, SBAR
       end do
 200   CONTINUE

       END



