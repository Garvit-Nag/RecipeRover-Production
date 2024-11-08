import { Client, Account, Databases, ID } from 'appwrite';

const client = new Client()
    .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT!)
    .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID!);

export const account = new Account(client);
export const databases = new Databases(client);

export const createUserDocument = async (
    userId: string,  // This will be user.$id from Appwrite
    name: string,
    email: string,
    avatar: string,
) => {
    try {
        const response = await databases.createDocument(
            process.env.NEXT_PUBLIC_APPWRITE_DATABASE_ID!,
            process.env.NEXT_PUBLIC_APPWRITE_USERS_COLLECTION_ID!,
            ID.unique(),  // Use the Appwrite ID directly
            {
                userId,  // Store the same ID
                name,
                email,
                avatar,
                createdAt: new Date().toISOString(),
                lastLogin: new Date().toISOString(),
            }
        );
        return response;
    } catch (error) {
        console.error('Error creating user document:', error);
        throw error;
    }
};

