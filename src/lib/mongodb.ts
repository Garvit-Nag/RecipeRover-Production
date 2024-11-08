// src/lib/mongodb.ts
import mongoose, { Model, Document } from 'mongoose';

// Interface for the search history document
interface ISearchHistory extends Document {
  userId: string;
  searchData: any;
  searchDate: Date;
  totalResults: number;
}

// Declare global mongoose cache
declare global {
  var mongoose: {
    conn: null | typeof mongoose;
    promise: null | Promise<typeof mongoose>;
  };
}

// Initialize cache
const globalMongoose = global as unknown as {
  mongoose: {
    conn: null | typeof mongoose;
    promise: null | Promise<typeof mongoose>;
  };
};

if (!globalMongoose.mongoose) {
  globalMongoose.mongoose = { conn: null, promise: null };
}

// Database connection function
export async function connectToDatabase() {
    console.log('[MongoDB] Starting database connection');

    try {
      const uri = process.env.NEXT_PUBLIC_MONGODB_URI;
      if (!uri) {
        console.error('[MongoDB] Missing MONGODB_URI environment variable');
        throw new Error('Missing MONGODB_URI environment variable');
      }

      // Log the database name from the connection string (with credentials removed)
      const dbName = uri.split('/').pop();
      console.log('[MongoDB] Connecting to database:', dbName);

      if (globalMongoose.mongoose.conn) {
        console.log('[MongoDB] Using existing connection');
        // Verify we're connected to the right database
        const connectedDb = globalMongoose.mongoose.conn.connection.db.databaseName;
        console.log('[MongoDB] Currently connected to database:', connectedDb);
        return globalMongoose.mongoose.conn;
      }

      if (!globalMongoose.mongoose.promise) {
        console.log('[MongoDB] Creating new connection');
        const opts = {
          bufferCommands: false,
        };

        globalMongoose.mongoose.promise = mongoose.connect(uri, opts);
      }

      console.log('[MongoDB] Awaiting connection');
      const conn = await globalMongoose.mongoose.promise;

      // Log connected database details
      const collections = await conn.connection.db.listCollections().toArray();
      console.log('[MongoDB] Available collections:', collections.map(c => c.name));

      globalMongoose.mongoose.conn = conn;
      console.log('[MongoDB] Connection successful');
      return conn;
    } catch (error) {
      console.error('[MongoDB] Connection error:', error);
      throw error;
    }
  }

// Schema definition
const SearchHistorySchema = new mongoose.Schema<ISearchHistory>({
  userId: {
    type: String,
    required: true,
    index: true
  },
  searchData: {
    type: mongoose.Schema.Types.Mixed,
    required: true
  },
  searchDate: {
    type: Date,
    default: Date.now
  },
  totalResults: {
    type: Number,
    required: true
  }
}, {
  timestamps: true
});

// Model creation with proper typing
export const SearchHistory: Model<ISearchHistory> = mongoose.models.SearchHistory || 
  mongoose.model<ISearchHistory>('SearchHistory', SearchHistorySchema);