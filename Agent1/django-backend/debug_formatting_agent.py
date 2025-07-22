"""
Debug test for FormattingAgent
"""
import os
import sys

# Add the django project to Python path
sys.path.append(r'c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend')

def test_formatting_agent_debug():
    """Debug the FormattingAgent"""
    try:
        from research_agent.formatting_agent import FormattingAgent
        
        print("✅ FormattingAgent imported successfully")
        
        agent = FormattingAgent()
        print("✅ FormattingAgent instantiated successfully")
        
        # Simple test data
        test_data = {
            'title': 'Test Report',
            'executive_summary': 'Test summary',
            'generated_at': '2025-01-01 12:00 UTC'
        }
        
        print("📄 Testing .docx generation...")
        docx_stream = agent.create_professional_docx_report(test_data, 'Test User')
        
        if docx_stream:
            # Get the size properly
            current_pos = docx_stream.tell()
            docx_stream.seek(0, 2)  # Seek to end
            size = docx_stream.tell()
            docx_stream.seek(current_pos)  # Restore position
            
            print(f"✅ .docx generated successfully! Size: {size:,} bytes")
            
            # Save test file
            test_file = r'c:\Users\t-tokelowo\OneDrive - Microsoft\Agent 1\django-backend\debug_test_report.docx'
            docx_stream.seek(0)
            with open(test_file, 'wb') as f:
                f.write(docx_stream.read())
            print(f"📁 Test file saved: {test_file}")
            
            return size > 0
        else:
            print("❌ .docx generation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debugging FormattingAgent")
    print("=" * 40)
    
    test_formatting_agent_debug()
