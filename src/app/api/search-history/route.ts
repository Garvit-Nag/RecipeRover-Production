import { NextResponse } from 'next/server';
import { connectToDatabase, SearchHistory } from '@/lib/mongodb';

export async function POST(request: Request) {
  try {
    console.log('[API Debug] Received POST request to /api/search-history');

    const body = await request.json();
    console.log('[API Debug] Request body:', {
      userId: body.userId,
      dataLength: body.searchData?.length,
      firstRecipe: body.searchData?.[0]?.Name
    });

    await connectToDatabase();
    console.log('[API Debug] Database connected successfully');

    const searchHistory = new SearchHistory({
      userId: body.userId,
      searchData: body.searchData,
      totalResults: body.searchData?.length || 0,
      searchDate: new Date()
    });

    console.log('[API Debug] Created SearchHistory document:', {
      userId: searchHistory.userId,
      totalResults: searchHistory.totalResults,
      searchDate: searchHistory.searchDate
    });

    const savedDoc = await searchHistory.save();
    console.log('[API Debug] Document saved successfully:', savedDoc._id);

    return NextResponse.json({ 
      success: true, 
      message: 'Search history saved',
      documentId: savedDoc._id 
    });
  } catch (error) {
    console.error('[API Error] Failed to save search history:', error);
    return NextResponse.json({ 
      error: 'Failed to save search history',
      details: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

export async function GET(request: Request) {
    console.log('[API] Starting GET request handling');

    try {
      const { searchParams } = new URL(request.url);
      const userId = searchParams.get('userId');
      console.log('[API] Received request for userId:', userId);

      if (!userId) {
        console.log('[API] No userId provided');
        return NextResponse.json({ error: 'UserId is required' }, { status: 400 });
      }

      console.log('[API] Attempting database connection');
      await connectToDatabase();
      console.log('[API] Database connected successfully');

      // First, let's check if the collection exists and get a count of all documents
      const totalCount = await SearchHistory.countDocuments({});
      console.log('[API] Total documents in collection:', totalCount);

      // Let's look at a sample of documents to verify the data structure
      const sampleDocs = await SearchHistory.find({}).limit(1).lean();
      console.log('[API] Sample document structure:', JSON.stringify(sampleDocs, null, 2));

      // Now query for this specific user
      console.log('[API] Querying search history for userId:', userId);
      const searchHistory = await SearchHistory.find({ userId })
        .sort({ searchDate: -1 })
        .lean();

      console.log('[API] Query results:', {
        queryUserId: userId,
        resultsFound: searchHistory.length,
        sampleUserIds: searchHistory.map(h => h.userId).slice(0, 3)
      });

      // If we didn't find anything, let's double check the userId format
      if (searchHistory.length === 0) {
        // Let's find what userIds exist in our collection
        const distinctUserIds = await SearchHistory.distinct('userId');
        console.log('[API] Distinct userIds in collection:', distinctUserIds);
      }

      return NextResponse.json(searchHistory);
    } catch (error) {
      console.error('[API] Error in GET request:', error);
      return NextResponse.json({ 
        error: 'Internal Server Error',
        details: error instanceof Error ? error.message : 'Unknown error'
      }, { status: 500 });
    }
  }