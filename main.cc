/***************************************************************************
 *            main.cc
 *
 *  
 *  Copyright  2005  Tristen Georgiou
 *  tristen_georgiou@hotmail.com
 ****************************************************************************/

/*
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#include <string.h>
#include "highgui.h"
#include "FastMatchTemplate.h"

const char* const resultWindowName = "Results";

int searchForParameter( const char*  param,
                        int          numArgs,
                        char**       argList );
                        
void printOptions( void );

int main( int argc, char** argv )
{
  if( argc < 5 )
  {
    printf( "\nERROR: Required arguments missing.\n" );
    printOptions();
    return 1;
  }

  int sourceParam = searchForParameter( "-s", argc, argv );
  if( sourceParam == -1 )
  {
    printf( "\nERROR: Source argument missing.\n" );
    return 1;
  }
  
  int targetParam = searchForParameter( "-t", argc, argv );
  if( targetParam == -1 )
  {
    printf( "\nERROR: Target argument missing.\n" );
    return 1;
  }
  
  int yParam = searchForParameter( "-y", argc, argv );
  int qParam = searchForParameter( "-q", argc, argv );  
    
  sourceParam++;
  IplImage* source = cvLoadImage( argv[sourceParam], -1 );
  
  if( source == NULL )
  {
    printf( "\nERROR: Could not load image %s.\n", argv[sourceParam] );
    return 2;
  }
  
  targetParam++;
  IplImage* target = cvLoadImage( argv[targetParam], -1 );
  
  if( target == NULL )
  {
    printf( "\nERROR: Could not load image %s.\n", argv[targetParam] );
    return 2;
  }
  
  qParam++;
  int quality = 90;
  if(argv[qParam]) {
      quality = atoi(argv[qParam]);
  }
      
  // perform the match
  vector<CvPoint> foundPointsList;
  vector<double> confidencesList;
  if( !FastMatchTemplate( *source, 
                          *target, 
                          &foundPointsList, 
                          &confidencesList,
                          quality,
                          true,
                          12 ) )
  {
    printf( "\nERROR: Fast match template failed.\n" );
    return 3;
  }
  
  int numPoints = foundPointsList.size();
  printf("%i", numPoints);   
  
  int numInBlankRow = 0;  
  int blankRowY = 108;
  
  yParam++;
  if(argv[yParam]) {
      blankRowY = atoi(argv[yParam]);
  }
  
  
  for( int currPoint = 0; currPoint < numPoints; currPoint++ )
  {
    const CvPoint& point = foundPointsList[currPoint];    
    if(point.y < blankRowY) {
        numInBlankRow++;
    }
  }
  
  if(numInBlankRow > 0) {
      printf("|%i", numInBlankRow);
  }
    
  // for( int currPoint = 0; currPoint < numPoints; currPoint++ )
  // {
  //   const CvPoint& point = foundPointsList[currPoint];
  //   
  //   // write the confidences to stdout
  //   printf( "\nTarget found at (%d, %d), with confidence = %3.3f %%.\n", 
  //           point.x, 
  //           point.y, 
  //           confidencesList[currPoint] );
  //   
  // }
  //                
  // 
  // // create a color image to draw on
  // IplImage* colorImage = NULL;
  // 
  // // if the original is a grayscale image, convert it to color
  // if( source->nChannels == 1 )
  // {
  //   colorImage = cvCreateImage( cvGetSize( source ), IPL_DEPTH_8U, 3 );
  //   cvCvtColor( source, colorImage, CV_GRAY2RGB );
  // }
  // else
  // {
  //   colorImage = cvCloneImage( source );
  // }
  // 
  // DrawFoundTargets( colorImage, 
  //                   cvGetSize( target ), 
  //                   foundPointsList, 
  //                   confidencesList );
  // 
  // cvNamedWindow( resultWindowName, CV_WINDOW_AUTOSIZE );
  // cvShowImage( resultWindowName, colorImage );
  // 
  // // wait for both windows to be closed before releasing images
  // cvWaitKey( 0 );
  // cvDestroyWindow( resultWindowName );
  // 
  // cvReleaseImage( &source );
  // cvReleaseImage( &target );
  // cvReleaseImage( &colorImage );
  
  

  return 0;
}

int searchForParameter( const char*  param,
                        int          numArgs,
                        char**       argList )
{
  for( int currArg = 0; currArg < numArgs; currArg++ )
  {
    if( strcmp( param, argList[currArg] ) == 0 )
    {
      return currArg;
    }
  }
  
  // argument not found
  return -1;
}

void printOptions( void )
{
  printf( "\nFAST MATCH TEMPLATE EXAMPLE PROGRAM\n" );
  printf( "-----------------------------------\n" );
  printf( "\nProgram arguments:\n\n" );
  printf( "     -s source image name (image to be searched)\n\n" );
  printf( "     -t target image name (image we are trying to find)\n\n" );
  printf( "Example: FastMatchTemplate -s source.bmp -t target.bmp\n\n" );
}
